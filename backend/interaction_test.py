import requests
import json
import sys

# 从文件读取token
def get_token():
    try:
        with open("token.txt", "r") as f:
            return f.read().strip()
    except:
        print("无法读取token，请先运行login_test.py")
        return None

def test_comment_creation(token):
    """测试发表评论功能"""
    print("\n测试发表评论功能...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "novel_id": 1,
        "content": "这是一条测试评论，小说很好看！"
    }
    
    response = requests.post(
        "http://localhost:5000/api/interaction/comment",
        headers=headers,
        json=data
    )
    
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response.status_code == 201

def test_get_novel_comments():
    """测试获取小说评论功能"""
    print("\n测试获取小说评论功能...")
    
    response = requests.get(
        "http://localhost:5000/api/interaction/comments/1"
    )
    
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response.status_code == 200

def test_collect_novel(token):
    """测试收藏小说功能"""
    print("\n测试收藏小说功能...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "novel_id": 1
    }
    
    response = requests.post(
        "http://localhost:5000/api/interaction/collection",
        headers=headers,
        json=data
    )
    
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response.status_code == 200

def test_get_user_collections(token):
    """测试获取用户收藏列表功能"""
    print("\n测试获取用户收藏列表...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(
        "http://localhost:5000/api/interaction/collection",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response.status_code == 200

def test_get_reading_history(token):
    """测试获取阅读历史功能"""
    print("\n测试获取阅读历史...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(
        "http://localhost:5000/api/interaction/history",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response.status_code == 200

def test_follow_user(token):
    """测试关注用户功能"""
    print("\n测试关注用户功能...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "user_id": 1  # 尝试关注ID为1的用户
    }
    
    response = requests.post(
        "http://localhost:5000/api/interaction/follow",
        headers=headers,
        json=data
    )
    
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response.status_code == 200

if __name__ == "__main__":
    token = get_token()
    if not token:
        sys.exit(1)
    
    print(f"使用token: {token[:20]}...")
    
    # 逐个测试功能，避免一个失败导致整个脚本终止
    try:
        comment_result = test_comment_creation(token)
    except Exception as e:
        print(f"发表评论测试异常: {e}")
        comment_result = False
    
    try:
        comments_result = test_get_novel_comments()
    except Exception as e:
        print(f"获取评论测试异常: {e}")
        comments_result = False
    
    try:
        collect_result = test_collect_novel(token)
    except Exception as e:
        print(f"收藏小说测试异常: {e}")
        collect_result = False
    
    try:
        collections_result = test_get_user_collections(token)
    except Exception as e:
        print(f"获取收藏列表测试异常: {e}")
        collections_result = False
    
    try:
        history_result = test_get_reading_history(token)
    except Exception as e:
        print(f"获取阅读历史测试异常: {e}")
        history_result = False
    
    try:
        follow_result = test_follow_user(token)
    except Exception as e:
        print(f"关注用户测试异常: {e}")
        follow_result = False
    
    results = {
        "发表评论": comment_result,
        "获取小说评论": comments_result,
        "收藏小说": collect_result,
        "获取用户收藏": collections_result,
        "获取阅读历史": history_result,
        "关注用户": follow_result
    }
    
    print("\n===== 测试结果汇总 =====")
    for test_name, success in results.items():
        print(f"{test_name}: {'✓ 成功' if success else '✗ 失败'}") 