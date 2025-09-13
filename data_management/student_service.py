"""
学生数据服务模块
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import Student, StudentCreate, StudentUpdate, StudentResponse, StudentListResponse, StudentQuery
import logging

logger = logging.getLogger(__name__)


class StudentService:
    """学生数据服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_student(self, student_data: StudentCreate) -> StudentResponse:
        """创建学生"""
        try:
            # 检查学号是否已存在
            existing = await self.get_student_by_student_id(student_data.student_id)
            if existing:
                raise ValueError(f"学号 {student_data.student_id} 已存在")
            
            # 创建学生记录
            student = Student(**student_data.dict())
            self.db.add(student)
            await self.db.commit()
            await self.db.refresh(student)
            
            return StudentResponse.from_orm(student)
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"创建学生失败: {str(e)}")
            raise
    
    async def get_student_by_id(self, student_id: int) -> Optional[StudentResponse]:
        """根据ID获取学生"""
        try:
            result = await self.db.execute(
                select(Student).where(Student.id == student_id)
            )
            student = result.scalar_one_or_none()
            
            if student:
                return StudentResponse.from_orm(student)
            return None
            
        except Exception as e:
            logger.error(f"获取学生失败: {str(e)}")
            raise
    
    async def get_student_by_student_id(self, student_id: str) -> Optional[StudentResponse]:
        """根据学号获取学生"""
        try:
            result = await self.db.execute(
                select(Student).where(Student.student_id == student_id)
            )
            student = result.scalar_one_or_none()
            
            if student:
                return StudentResponse.from_orm(student)
            return None
            
        except Exception as e:
            logger.error(f"根据学号获取学生失败: {str(e)}")
            raise
    
    async def update_student(self, student_id: int, student_data: StudentUpdate) -> Optional[StudentResponse]:
        """更新学生信息"""
        try:
            result = await self.db.execute(
                select(Student).where(Student.id == student_id)
            )
            student = result.scalar_one_or_none()
            
            if not student:
                return None
            
            # 更新字段
            update_data = student_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(student, field, value)
            
            await self.db.commit()
            await self.db.refresh(student)
            
            return StudentResponse.from_orm(student)
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"更新学生失败: {str(e)}")
            raise
    
    async def delete_student(self, student_id: int) -> bool:
        """删除学生（软删除）"""
        try:
            result = await self.db.execute(
                select(Student).where(Student.id == student_id)
            )
            student = result.scalar_one_or_none()
            
            if not student:
                return False
            
            student.is_active = False
            await self.db.commit()
            
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"删除学生失败: {str(e)}")
            raise
    
    async def list_students(self, query: StudentQuery) -> StudentListResponse:
        """查询学生列表"""
        try:
            # 构建查询条件
            conditions = []
            
            if query.student_id:
                conditions.append(Student.student_id.like(f"%{query.student_id}%"))
            if query.name:
                conditions.append(Student.name.like(f"%{query.name}%"))
            if query.class_name:
                conditions.append(Student.class_name == query.class_name)
            if query.grade:
                conditions.append(Student.grade == query.grade)
            if query.major:
                conditions.append(Student.major == query.major)
            if query.is_active is not None:
                conditions.append(Student.is_active == query.is_active)
            if query.created_after:
                conditions.append(Student.created_at >= query.created_after)
            if query.created_before:
                conditions.append(Student.created_at <= query.created_before)
            
            # 查询总数
            count_query = select(func.count(Student.id))
            if conditions:
                count_query = count_query.where(*conditions)
            
            total_result = await self.db.execute(count_query)
            total = total_result.scalar()
            
            # 查询数据
            data_query = select(Student)
            if conditions:
                data_query = data_query.where(*conditions)
            
            data_query = data_query.offset((query.page - 1) * query.page_size).limit(query.page_size)
            
            result = await self.db.execute(data_query)
            students = result.scalars().all()
            
            # 转换为响应模型
            student_responses = [StudentResponse.from_orm(student) for student in students]
            
            return StudentListResponse(
                students=student_responses,
                total=total,
                page=query.page,
                page_size=query.page_size,
                total_pages=(total + query.page_size - 1) // query.page_size
            )
            
        except Exception as e:
            logger.error(f"查询学生列表失败: {str(e)}")
            raise
    
    async def batch_create_students(self, students_data: List[StudentCreate]) -> dict:
        """批量创建学生"""
        try:
            created_count = 0
            skipped_count = 0
            errors = []
            
            for student_data in students_data:
                try:
                    # 检查学号是否已存在
                    existing = await self.get_student_by_student_id(student_data.student_id)
                    if existing:
                        skipped_count += 1
                        continue
                    
                    # 创建学生
                    student = Student(**student_data.dict())
                    self.db.add(student)
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"学号 {student_data.student_id}: {str(e)}")
            
            if created_count > 0:
                await self.db.commit()
            
            return {
                "created_count": created_count,
                "skipped_count": skipped_count,
                "error_count": len(errors),
                "errors": errors
            }
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"批量创建学生失败: {str(e)}")
            raise
    
    async def get_students_by_class(self, class_name: str) -> List[StudentResponse]:
        """获取班级学生列表"""
        try:
            result = await self.db.execute(
                select(Student).where(
                    Student.class_name == class_name,
                    Student.is_active == True
                )
            )
            students = result.scalars().all()
            
            return [StudentResponse.from_orm(student) for student in students]
            
        except Exception as e:
            logger.error(f"获取班级学生失败: {str(e)}")
            raise
    
    async def get_student_statistics(self) -> dict:
        """获取学生统计信息"""
        try:
            # 总学生数
            total_result = await self.db.execute(select(func.count(Student.id)))
            total_students = total_result.scalar()
            
            # 活跃学生数
            active_result = await self.db.execute(
                select(func.count(Student.id)).where(Student.is_active == True)
            )
            active_students = active_result.scalar()
            
            # 按班级统计
            class_result = await self.db.execute(
                select(Student.class_name, func.count(Student.id))
                .where(Student.is_active == True)
                .group_by(Student.class_name)
            )
            class_stats = {row[0]: row[1] for row in class_result.all()}
            
            # 按年级统计
            grade_result = await self.db.execute(
                select(Student.grade, func.count(Student.id))
                .where(Student.is_active == True)
                .group_by(Student.grade)
            )
            grade_stats = {row[0]: row[1] for row in grade_result.all()}
            
            return {
                "total_students": total_students,
                "active_students": active_students,
                "inactive_students": total_students - active_students,
                "class_distribution": class_stats,
                "grade_distribution": grade_stats
            }
            
        except Exception as e:
            logger.error(f"获取学生统计失败: {str(e)}")
            raise