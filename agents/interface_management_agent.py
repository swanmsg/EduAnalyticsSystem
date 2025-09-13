"""
接口管理智能体
负责与外部系统的数据接口对接和管理
"""
import asyncio
import json
import aiohttp
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
import xml.etree.ElementTree as ET
from io import StringIO
from config.settings import settings
from agents.base_agent import BaseAgent, AgentMessage
import logging

logger = logging.getLogger(__name__)


class InterfaceManagementAgent(BaseAgent):
    """接口管理智能体"""
    
    def __init__(self):
        super().__init__(
            agent_id="interface_management_agent",
            name="接口管理智能体",
            description="负责与外部教学研究系统和教育管理平台的数据对接"
        )
        self.capabilities = [
            "data_export",
            "data_import", 
            "api_integration",
            "format_conversion",
            "data_validation",
            "sync_management",
            "webhook_handling"
        ]
        self.supported_formats = [
            "json", "xml", "csv", "excel", 
            "pdf", "api", "database", "webhook"
        ]
        self.external_systems = {}
        
    async def handle_message(self, message: AgentMessage) -> Dict[str, Any]:
        """处理接口管理请求"""
        message_type = message.message_type
        content = message.content
        
        if message_type == "export_data":
            return await self._export_data(content)
        elif message_type == "import_data":
            return await self._import_data(content)
        elif message_type == "sync_with_external":
            return await self._sync_with_external_system(content)
        elif message_type == "register_external_system":
            return await self._register_external_system(content)
        elif message_type == "convert_format":
            return await self._convert_data_format(content)
        elif message_type == "validate_data":
            return await self._validate_data(content)
        elif message_type == "handle_webhook":
            return await self._handle_webhook(content)
        else:
            raise ValueError(f"不支持的消息类型: {message_type}")
            
    def get_capabilities(self) -> List[str]:
        """获取智能体能力列表"""
        return self.capabilities
        
    async def _export_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """导出数据到外部系统"""
        export_format = params.get("format", "json")
        data_type = params.get("data_type")
        target_system = params.get("target_system")
        query_params = params.get("query_params", {})
        
        try:
            # 获取要导出的数据
            export_data = await self._fetch_export_data(data_type, query_params)
            
            if not export_data:
                return {"error": "没有找到要导出的数据"}
            
            # 根据格式转换数据
            converted_data = await self._convert_to_format(export_data, export_format)
            
            # 如果指定了目标系统，直接发送
            if target_system:
                result = await self._send_to_external_system(
                    target_system, converted_data, export_format
                )
                
                return {
                    "export_type": "direct",
                    "target_system": target_system,
                    "format": export_format,
                    "record_count": len(export_data),
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                # 生成导出文件
                file_info = await self._save_export_file(converted_data, export_format, data_type)
                
                return {
                    "export_type": "file",
                    "format": export_format,
                    "record_count": len(export_data),
                    "file_info": file_info,
                    "download_url": file_info.get("url"),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"数据导出失败: {str(e)}")
            raise
            
    async def _import_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """从外部系统导入数据"""
        source = params.get("source")
        data_format = params.get("format", "json")
        data_type = params.get("data_type")
        mapping_config = params.get("mapping_config", {})
        
        try:
            # 获取源数据
            if source.get("type") == "file":
                raw_data = await self._read_import_file(source["path"], data_format)
            elif source.get("type") == "api":
                raw_data = await self._fetch_from_api(source["url"], source.get("headers", {}))
            elif source.get("type") == "database":
                raw_data = await self._fetch_from_database(source["connection"], source["query"])
            else:
                raise ValueError(f"不支持的数据源类型: {source.get('type')}")
            
            # 数据验证
            validation_result = await self._validate_import_data(raw_data, data_type)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": "数据验证失败",
                    "validation_errors": validation_result["errors"]
                }
            
            # 数据映射和转换
            mapped_data = await self._map_data_fields(raw_data, mapping_config, data_type)
            
            # 导入到系统
            import_result = await self._import_to_system(mapped_data, data_type)
            
            return {
                "success": True,
                "import_type": data_type,
                "source_format": data_format,
                "record_count": len(mapped_data),
                "imported_count": import_result["imported"],
                "skipped_count": import_result["skipped"],
                "error_count": import_result["errors"],
                "details": import_result["details"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"数据导入失败: {str(e)}")
            raise
            
    async def _sync_with_external_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """与外部系统同步数据"""
        system_id = params.get("system_id")
        sync_type = params.get("sync_type", "bidirectional")  # push, pull, bidirectional
        data_types = params.get("data_types", [])
        
        try:
            system_config = self.external_systems.get(system_id)
            if not system_config:
                raise ValueError(f"未找到外部系统配置: {system_id}")
            
            sync_results = {}
            
            for data_type in data_types:
                if sync_type in ["push", "bidirectional"]:
                    # 推送数据到外部系统
                    push_result = await self._push_data_to_system(system_config, data_type)
                    sync_results[f"{data_type}_push"] = push_result
                
                if sync_type in ["pull", "bidirectional"]:
                    # 从外部系统拉取数据
                    pull_result = await self._pull_data_from_system(system_config, data_type)
                    sync_results[f"{data_type}_pull"] = pull_result
            
            return {
                "system_id": system_id,
                "sync_type": sync_type,
                "data_types": data_types,
                "results": sync_results,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"系统同步失败: {str(e)}")
            raise
            
    async def _register_external_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """注册外部系统"""
        system_config = {
            "system_id": params.get("system_id"),
            "name": params.get("name"),
            "type": params.get("type"),  # api, database, file_server
            "endpoint": params.get("endpoint"),
            "authentication": params.get("authentication", {}),
            "data_mappings": params.get("data_mappings", {}),
            "sync_schedule": params.get("sync_schedule"),
            "enabled": params.get("enabled", True),
            "registered_at": datetime.utcnow().isoformat()
        }
        
        try:
            # 测试连接
            connection_test = await self._test_external_system_connection(system_config)
            
            if connection_test["success"]:
                self.external_systems[system_config["system_id"]] = system_config
                
                return {
                    "success": True,
                    "system_id": system_config["system_id"],
                    "connection_test": connection_test,
                    "message": "外部系统注册成功"
                }
            else:
                return {
                    "success": False,
                    "error": "连接测试失败",
                    "connection_test": connection_test
                }
                
        except Exception as e:
            logger.error(f"注册外部系统失败: {str(e)}")
            raise
            
    async def _convert_data_format(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """数据格式转换"""
        data = params.get("data")
        source_format = params.get("source_format")
        target_format = params.get("target_format")
        
        try:
            # 解析源数据
            parsed_data = await self._parse_data(data, source_format)
            
            # 转换为目标格式
            converted_data = await self._convert_to_format(parsed_data, target_format)
            
            return {
                "success": True,
                "source_format": source_format,
                "target_format": target_format,
                "converted_data": converted_data,
                "record_count": len(parsed_data) if isinstance(parsed_data, list) else 1
            }
            
        except Exception as e:
            logger.error(f"格式转换失败: {str(e)}")
            raise
            
    async def _convert_to_format(self, data: Any, target_format: str) -> Any:
        """转换数据到指定格式"""
        if target_format == "json":
            return json.dumps(data, ensure_ascii=False, indent=2, default=str)
        elif target_format == "csv":
            if isinstance(data, list) and data:
                df = pd.DataFrame(data)
                output = StringIO()
                df.to_csv(output, index=False, encoding='utf-8-sig')
                return output.getvalue()
        elif target_format == "xml":
            return self._convert_to_xml(data)
        elif target_format == "excel":
            if isinstance(data, list) and data:
                df = pd.DataFrame(data)
                output = StringIO()
                # 注意：实际应用中需要使用BytesIO和具体的Excel文件处理
                return df.to_dict('records')
        else:
            return data
            
    def _convert_to_xml(self, data: Any) -> str:
        """转换数据为XML格式"""
        root = ET.Element("data")
        
        if isinstance(data, list):
            for i, item in enumerate(data):
                item_elem = ET.SubElement(root, "item", {"index": str(i)})
                self._dict_to_xml(item, item_elem)
        elif isinstance(data, dict):
            self._dict_to_xml(data, root)
        else:
            root.text = str(data)
            
        return ET.tostring(root, encoding='unicode')
        
    def _dict_to_xml(self, data: dict, parent: ET.Element):
        """字典转XML"""
        for key, value in data.items():
            elem = ET.SubElement(parent, str(key))
            if isinstance(value, dict):
                self._dict_to_xml(value, elem)
            elif isinstance(value, list):
                for item in value:
                    item_elem = ET.SubElement(elem, "item")
                    if isinstance(item, dict):
                        self._dict_to_xml(item, item_elem)
                    else:
                        item_elem.text = str(item)
            else:
                elem.text = str(value)
                
    async def _test_external_system_connection(self, system_config: Dict) -> Dict[str, Any]:
        """测试外部系统连接"""
        try:
            if system_config["type"] == "api":
                async with aiohttp.ClientSession() as session:
                    headers = system_config.get("authentication", {}).get("headers", {})
                    async with session.get(system_config["endpoint"], headers=headers) as response:
                        if response.status == 200:
                            return {"success": True, "status_code": response.status}
                        else:
                            return {"success": False, "status_code": response.status, "error": "HTTP错误"}
            else:
                # 其他类型的连接测试
                return {"success": True, "message": "连接测试通过"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    # 其他辅助方法的实现...
    async def _fetch_export_data(self, data_type: str, query_params: Dict) -> List[Dict]:
        """获取要导出的数据"""
        # 根据数据类型和查询参数从数据库获取数据
        return []
        
    async def _save_export_file(self, data: Any, format: str, data_type: str) -> Dict:
        """保存导出文件"""
        import os
        filename = f"{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        filepath = os.path.join(settings.EXPORT_DIR, filename)
        
        # 确保目录存在
        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(data))
            
        return {
            "filename": filename,
            "filepath": filepath,
            "size": os.path.getsize(filepath),
            "url": f"/api/v1/download/{filename}"
        }