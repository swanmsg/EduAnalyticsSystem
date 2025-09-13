"""
学生管理API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_async_db
from models import (
    StudentCreate, StudentUpdate, StudentResponse, 
    StudentListResponse, StudentQuery
)
from data_management.student_service import StudentService

router = APIRouter()


@router.post("/", response_model=StudentResponse, summary="创建学生")
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """创建新学生"""
    try:
        service = StudentService(db)
        student = await service.create_student(student_data)
        return student
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{student_id}", response_model=StudentResponse, summary="获取学生详情")
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """根据ID获取学生详情"""
    try:
        service = StudentService(db)
        student = await service.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="学生不存在")
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{student_id}", response_model=StudentResponse, summary="更新学生信息")
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """更新学生信息"""
    try:
        service = StudentService(db)
        student = await service.update_student(student_id, student_data)
        if not student:
            raise HTTPException(status_code=404, detail="学生不存在")
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{student_id}", summary="删除学生")
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """删除学生（软删除）"""
    try:
        service = StudentService(db)
        success = await service.delete_student(student_id)
        if not success:
            raise HTTPException(status_code=404, detail="学生不存在")
        return {"message": "学生删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=StudentListResponse, summary="查询学生列表")
async def list_students(
    student_id: str = Query(None, description="学号"),
    name: str = Query(None, description="学生姓名"),
    class_name: str = Query(None, description="班级"),
    grade: str = Query(None, description="年级"),
    major: str = Query(None, description="专业"),
    is_active: bool = Query(None, description="是否激活"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_async_db)
):
    """查询学生列表"""
    try:
        query_params = StudentQuery(
            student_id=student_id,
            name=name,
            class_name=class_name,
            grade=grade,
            major=major,
            is_active=is_active,
            page=page,
            page_size=page_size
        )
        
        service = StudentService(db)
        result = await service.list_students(query_params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/student-id/{student_id}", response_model=StudentResponse, summary="根据学号获取学生")
async def get_student_by_student_id(
    student_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """根据学号获取学生信息"""
    try:
        service = StudentService(db)
        student = await service.get_student_by_student_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="学生不存在")
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", summary="批量创建学生")
async def batch_create_students(
    students_data: List[StudentCreate],
    db: AsyncSession = Depends(get_async_db)
):
    """批量创建学生"""
    try:
        service = StudentService(db)
        result = await service.batch_create_students(students_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/class/{class_name}/students", response_model=List[StudentResponse], summary="获取班级学生列表")
async def get_students_by_class(
    class_name: str,
    db: AsyncSession = Depends(get_async_db)
):
    """获取指定班级的所有学生"""
    try:
        service = StudentService(db)
        students = await service.get_students_by_class(class_name)
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics/overview", summary="学生统计概览")
async def get_student_statistics(
    db: AsyncSession = Depends(get_async_db)
):
    """获取学生统计概览"""
    try:
        service = StudentService(db)
        stats = await service.get_student_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))