import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """运行数据库迁移"""
    print("开始数据库迁移...")
    
    # 设置环境变量
    os.environ['FLASK_APP'] = 'app'
    
    try:
        # 创建migrations目录(如果不存在)
        migrations_dir = Path(__file__).parent.parent / 'migrations'
        versions_dir = migrations_dir / 'versions'
        if not versions_dir.exists():
            versions_dir.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {versions_dir}")
            
        # 执行迁移
        subprocess.run(['flask', 'db', 'upgrade'], check=True)
        print("数据库迁移完成!")
    except Exception as e:
        print(f"迁移失败: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 