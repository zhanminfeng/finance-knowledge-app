import json
import os
from typing import Dict, List, TypeVar, Generic, Type, Optional, Any
from pathlib import Path
from pydantic import BaseModel

from app.core.config import settings
from app.core.logging import logger

# 定义泛型类型变量，限制为BaseModel的子类
T = TypeVar('T', bound=BaseModel)


class DataService(Generic[T]):
    """通用数据访问服务，处理JSON文件的读写操作"""
    
    def __init__(self, file_name: str, model_class: Type[T]):
        """
        初始化数据服务
        
        Args:
            file_name: 数据文件名
            model_class: 数据模型类
        """
        self.file_path = settings.DATA_DIR / file_name
        self.model_class = model_class
        self._data: List[Dict[str, Any]] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """从JSON文件加载数据"""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                logger.info(f"成功从 {self.file_path} 加载了 {len(self._data)} 条数据")
            else:
                logger.warning(f"数据文件 {self.file_path} 不存在")
                self._data = []
        except Exception as e:
            logger.error(f"加载数据文件 {self.file_path} 失败: {str(e)}")
            self._data = []
    
    def get_all(self) -> List[T]:
        """获取所有数据项"""
        return [self.model_class(**item) for item in self._data]
    
    def get_by_id(self, item_id: str) -> Optional[T]:
        """根据ID获取特定数据项"""
        for item in self._data:
            if item.get('id') == item_id:
                return self.model_class(**item)
        return None
    
    def search(self, keyword: str) -> List[T]:
        """
        搜索数据项
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            符合条件的数据项列表
        """
        result = []
        keyword = keyword.lower()
        
        for item in self._data:
            # 搜索所有字符串字段
            for key, value in item.items():
                if isinstance(value, str) and keyword in value.lower():
                    result.append(self.model_class(**item))
                    break
        
        return result
    
    def save_data(self, data: List[T]) -> bool:
        """
        保存数据到JSON文件
        
        Args:
            data: 要保存的数据列表
            
        Returns:
            保存是否成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
            # 将模型对象转换为字典
            data_dicts = [item.dict() for item in data]
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data_dicts, f, ensure_ascii=False, indent=2)
            
            logger.info(f"成功保存 {len(data)} 条数据到 {self.file_path}")
            self._data = data_dicts
            return True
        except Exception as e:
            logger.error(f"保存数据到 {self.file_path} 失败: {str(e)}")
            return False 