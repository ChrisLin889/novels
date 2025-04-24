# 管理模块 API 测试报告

**测试时间**: 2025-04-24 10:23:32

**测试脚本**: test_admin_api.py

## 测试结果汇总


================================================================================
测试: 注册普通用户
================================================================================
注册用户: testuser_9352, 邮箱: test_user_3943@example.com, 手机: 144547113
状态码: 201
响应内容: {
  "message": "User registered successfully",
  "success": true,
  "user": {
    "created_at": "2025-04-24T02:23:32",
    "email": "test_user_3943@example.com",
    "id": 42,
    "phone": "144547113",
    "username": "testuser_9352"
  }
}
✅ 成功: 用户注册成功，用户ID: 42

================================================================================
测试: 普通用户登录
================================================================================
登录用户: testuser_9352
状态码: 200
响应内容: {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTQ2MTQxMiwianRpIjoiNTRiMTUxNWQtZmNiMS00YjNlLTkxODktNjMyYjJhNDEwODBjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NDIsIm5iZiI6MTc0NTQ2MTQxMiwiZXhwIjoxNzQ2MDY2MjEyLCJyb2xlIjoidXNlciJ9.JFeVXkGQq5l2zWVfn-ybFkgQf4LfTAoQamxBAtmV3PU",
  "success": true,
  "user": {
    "avatar": "default.jpg",
    "created_at": "2025-04-24T02:23:32",
    "email": "test_user_3943@example.com",
    "id": 42,
    "phone": "144547113",
    "role": "user",
    "status": "active",
    "updated_at": "2025-04-24T10:23:33",
    "username": "testuser_9352"
  }
}
✅ 成功: 普通用户登录成功

================================================================================
测试: 注册将成为作者的用户
================================================================================
注册用户: testauthor_6245, 邮箱: test_author_3857@example.com, 手机: 183352312
状态码: 201
响应内容: {
  "message": "User registered successfully",
  "success": true,
  "user": {
    "created_at": "2025-04-24T02:23:33",
    "email": "test_author_3857@example.com",
    "id": 43,
    "phone": "183352312",
    "username": "testauthor_6245"
  }
}
✅ 成功: 用户注册成功，用户ID: 43

================================================================================
测试: 将成为作者的用户登录
================================================================================
登录用户: testauthor_6245
状态码: 200
响应内容: {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTQ2MTQxMiwianRpIjoiZWIwMzc1OTQtOGE5OC00NTI2LWFkZmYtNDkwNTA5OWViYjkzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NDMsIm5iZiI6MTc0NTQ2MTQxMiwiZXhwIjoxNzQ2MDY2MjEyLCJyb2xlIjoidXNlciJ9.i-HCe38JBr_R0Jhc_Xf84FIUHgLTQ0XD84P8Zrk6w0Y",
  "success": true,
  "user": {
    "avatar": "default.jpg",
    "created_at": "2025-04-24T02:23:33",
    "email": "test_author_3857@example.com",
    "id": 43,
    "phone": "183352312",
    "role": "user",
    "status": "active",
    "updated_at": "2025-04-24T10:23:33",
    "username": "testauthor_6245"
  }
}
✅ 成功: 用户登录成功

================================================================================
测试: 管理员登录
================================================================================
登录管理员: newadmin
状态码: 200
响应内容: {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTQ2MTQxMywianRpIjoiNmJkZDFkODQtZjAzOC00ZThhLThkYTYtN2IwMDVjYTM1ZDE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NiwibmJmIjoxNzQ1NDYxNDEzLCJleHAiOjE3NDYwNjYyMTMsInJvbGUiOiJhZG1pbiJ9.hTs0NdYqcCq42muPmwBlyAk7VmxFnQwJ7AAns-uZpIE",
  "success": true,
  "user": {
    "admin": {
      "admin_level": 1,
      "department": null,
      "id": 2,
      "permissions": {
        "content": true,
        "user": true
      }
    },
    "avatar": "default.jpg",
    "created_at": "2025-04-18T19:30:44",
    "email": "newadmin@test.com",
    "id": 6,
    "phone": "12345678900",
    "role": "admin",
    "status": "active",
    "updated_at": "2025-04-24T10:23:33",
    "username": "newadmin"
  }
}
✅ 成功: 管理员登录成功

================================================================================
测试: 获取管理员仪表盘数据
================================================================================
获取仪表盘数据...
状态码: 200
响应内容: {
  "activity_stats": {
    "comments_today": 0,
    "readings_today": "2"
  },
  "content_stats": {
    "pending_moderation": 0,
    "rejected_content": 0,
    "total_chapters": 8,
    "total_novels": 8
  },
  "user_stats": {
    "active_users_today": 11,
    "banned_users": 0,
    "new_users_today": 4,
    "total_users": 13
  }
}
✅ 成功: 成功获取仪表盘数据

================================================================================
测试: 获取用户列表
================================================================================
获取用户列表...
状态码: 200
响应内容: {
  "page": 1,
  "per_page": 20,
  "total": 13,
  "total_pages": 1,
  "users": [
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-24T02:23:33",
      "email": "test_author_3857@example.com",
      "id": 43,
      "phone": "183352312",
      "role": "user",
      "status": "active",
      "username": "testauthor_6245"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-24T02:23:32",
      "email": "test_user_3943@example.com",
      "id": 42,
      "phone": "144547113",
      "role": "user",
      "status": "active",
      "username": "testuser_9352"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-24T02:11:47",
      "email": "test_author_2733@example.com",
      "id": 41,
      "phone": "171410367",
      "role": "user",
      "status": "active",
      "username": "testauthor_7364"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-24T01:43:02",
      "email": "test_author_1662@example.com",
      "id": 37,
      "phone": "179616748",
      "role": "user",
      "status": "active",
      "username": "testauthor_5912"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-23T23:56:02",
      "email": "test_author_8223@example.com",
      "id": 34,
      "phone": "136996572",
      "role": "user",
      "status": "active",
      "username": "testauthor_4852"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-20T21:56:09",
      "email": "testauthor2@example.com",
      "id": 28,
      "phone": "13900139000",
      "role": "user",
      "status": "active",
      "username": "testauthor2"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-20T21:56:04",
      "email": "testauthor1@example.com",
      "id": 27,
      "phone": null,
      "role": "user",
      "status": "active",
      "username": "testauthor1"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-20T21:55:59",
      "email": null,
      "id": 26,
      "phone": "13800138000",
      "role": "user",
      "status": "active",
      "username": "testuser3"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-20T21:55:53",
      "email": "testuser2@example.com",
      "id": 25,
      "phone": null,
      "role": "user",
      "status": "active",
      "username": "testuser2"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-20T21:55:47",
      "email": "testuser1@example.com",
      "id": 24,
      "phone": null,
      "role": "user",
      "status": "active",
      "username": "testuser1"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-18T19:30:44",
      "email": "newadmin@test.com",
      "id": 6,
      "phone": "12345678900",
      "role": "admin",
      "status": "active",
      "username": "newadmin"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-18T19:13:56",
      "email": "author@test.com",
      "id": 5,
      "phone": "12345678902",
      "role": "author",
      "status": "active",
      "username": "testauthor"
    },
    {
      "avatar": "default.jpg",
      "banned_until": null,
      "created_at": "2025-04-18T19:13:49",
      "email": "updated.user@test.com",
      "id": 4,
      "phone": "12345678901",
      "role": "user",
      "status": "active",
      "username": "testuser"
    }
  ]
}
✅ 成功: 成功获取用户列表，且包含新注册的用户

================================================================================
测试: 提交第一次作者申请
================================================================================
申请作者: 笔名_6139
状态码: 201
响应内容: {
  "application": {
    "admin_comment": null,
    "admin_id": null,
    "bio": "这是一个测试作者简介，用于测试作者申请功能。",
    "created_at": "2025-04-24T02:23:33",
    "id": 15,
    "pen_name": "笔名_6139",
    "reason": "这是第一次申请，将被拒绝。",
    "status": "pending",
    "updated_at": "2025-04-24T02:23:33",
    "user_id": 43,
    "user_name": "testauthor_6245"
  },
  "message": "作者申请提交成功，请等待管理员审核"
}
✅ 成功: 作者申请提交成功，申请ID: 15

================================================================================
测试: 管理员获取待处理作者申请
================================================================================
管理员获取待处理作者申请...
状态码: 200
响应内容: {
  "applications": [
    {
      "admin_comment": null,
      "admin_id": null,
      "bio": "这是一个测试作者简介，用于测试作者申请功能。",
      "created_at": "2025-04-24T02:23:33",
      "id": 15,
      "pen_name": "笔名_6139",
      "reason": "这是第一次申请，将被拒绝。",
      "status": "pending",
      "updated_at": "2025-04-24T02:23:33",
      "user_id": 43,
      "user_name": "testauthor_6245"
    }
  ],
  "current_page": 1,
  "pages": 1,
  "total": 1
}
✅ 成功: 成功获取作者申请列表，且包含新提交的申请

================================================================================
测试: 管理员拒绝作者申请
================================================================================
拒绝作者申请 ID: 15
状态码: 200
响应内容: {
  "application": {
    "admin_comment": "测试拒绝作者申请，请完善申请资料后再次提交",
    "admin_id": 2,
    "bio": "这是一个测试作者简介，用于测试作者申请功能。",
    "created_at": "2025-04-24T02:23:33",
    "id": 15,
    "pen_name": "笔名_6139",
    "reason": "这是第一次申请，将被拒绝。",
    "status": "rejected",
    "updated_at": "2025-04-24T02:23:33",
    "user_id": 43,
    "user_name": "testauthor_6245"
  },
  "message": "申请已拒绝"
}
✅ 成功: 成功拒绝作者申请

================================================================================
测试: 提交第二次作者申请
================================================================================
再次申请作者: 优秀笔名_6387
状态码: 201
响应内容: {
  "application": {
    "admin_comment": null,
    "admin_id": null,
    "bio": "这是一个更详细的作者简介，包含我的写作经历和风格特点。",
    "created_at": "2025-04-24T02:23:33",
    "id": 16,
    "pen_name": "优秀笔名_6387",
    "reason": "这是第二次申请，已根据管理员意见完善了申请资料。",
    "status": "pending",
    "updated_at": "2025-04-24T02:23:33",
    "user_id": 43,
    "user_name": "testauthor_6245"
  },
  "message": "作者申请提交成功，请等待管理员审核"
}
✅ 成功: 第二次作者申请提交成功，申请ID: 16

================================================================================
测试: 管理员批准作者申请
================================================================================
批准作者申请 ID: 16
状态码: 200
响应内容: {
  "application": {
    "admin_comment": "申请资料完整，批准成为作者",
    "admin_id": 2,
    "bio": "这是一个更详细的作者简介，包含我的写作经历和风格特点。",
    "created_at": "2025-04-24T02:23:33",
    "id": 16,
    "pen_name": "优秀笔名_6387",
    "reason": "这是第二次申请，已根据管理员意见完善了申请资料。",
    "status": "approved",
    "updated_at": "2025-04-24T02:23:33",
    "user_id": 43,
    "user_name": "testauthor_6245"
  },
  "message": "申请已批准，用户已成为作者"
}
✅ 成功: 成功批准作者申请

================================================================================
测试: 更新用户角色
================================================================================
将用户 42 角色更新为作者
状态码: 200
响应内容: {
  "message": "User role updated to author",
  "success": true,
  "user": {
    "avatar": "default.jpg",
    "banned_until": null,
    "created_at": "2025-04-24T02:23:32",
    "email": "test_user_3943@example.com",
    "id": 42,
    "phone": "144547113",
    "role": "author",
    "status": "active",
    "username": "testuser_9352"
  }
}
✅ 成功: 成功更新用户角色为作者

================================================================================
测试: 管理用户状态
================================================================================
禁用用户 42，时长1天
状态码: 500
响应内容: <!doctype html>
<html lang=en>
  <head>
    <title>sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1452, &#39;Cannot add or update a child row: a foreign key constraint fails (`novel_db`.`user_action`, CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`))&#39;)
[SQL: INSERT INTO user_action (admin_id, target_user_id, action_type, reason, duration, created_at) VALUES (%(admin_id)s, %(target_user_id)s, %(action_type)s, %(reason)s, %(duration)s, %(created_at)s)]
[parameters: {&#39;admin_id&#39;: 6, &#39;target_user_id&#39;: 42, &#39;action_type&#39;: &#39;ban&#39;, &#39;reason&#39;: &#39;测试禁用功能&#39;, &#39;duration&#39;: 1, &#39;created_at&#39;: datetime.datetime(2025, 4, 24, 2, 23, 33, 351796)}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
 // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css">
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script>
      var CONSOLE_MODE = false,
          EVALEX = true,
          EVALEX_TRUSTED = false,
          SECRET = "hGZxCLme2nil2UPZIPjG";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
<h1>IntegrityError</h1>
<div class="detail">
  <p class="errormsg">sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1452, &#39;Cannot add or update a child row: a foreign key constraint fails (`novel_db`.`user_action`, CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`))&#39;)
[SQL: INSERT INTO user_action (admin_id, target_user_id, action_type, reason, duration, created_at) VALUES (%(admin_id)s, %(target_user_id)s, %(action_type)s, %(reason)s, %(duration)s, %(created_at)s)]
[parameters: {&#39;admin_id&#39;: 6, &#39;target_user_id&#39;: 42, &#39;action_type&#39;: &#39;ban&#39;, &#39;reason&#39;: &#39;测试禁用功能&#39;, &#39;duration&#39;: 1, &#39;created_at&#39;: datetime.datetime(2025, 4, 24, 2, 23, 33, 351796)}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
</p>
</div>
<h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
<div class="traceback">
  <h3></h3>
  <ul><li><div class="frame" id="frame-139743861633792">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1964</em>,
      in <code class="function">_exec_single_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                            </span>context,</pre>
<pre class="line before"><span class="ws">                        </span>):</pre>
<pre class="line before"><span class="ws">                            </span>evt_handled = True</pre>
<pre class="line before"><span class="ws">                            </span>break</pre>
<pre class="line before"><span class="ws">                </span>if not evt_handled:</pre>
<pre class="line current"><span class="ws">                    </span>self.dialect.do_execute(</pre>
<pre class="line after"><span class="ws">                        </span>cursor, str_statement, effective_parameters, context</pre>
<pre class="line after"><span class="ws">                    </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if self._has_events or self.engine._has_events:</pre>
<pre class="line after"><span class="ws">                </span>self.dispatch.after_cursor_execute(</pre></div>
</div>

<li><div class="frame" id="frame-139743861633904">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py"</cite>,
      line <em class="line">945</em>,
      in <code class="function">do_execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_executemany(self, cursor, statement, parameters, context=None):</pre>
<pre class="line before"><span class="ws">        </span>cursor.executemany(statement, parameters)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_execute(self, cursor, statement, parameters, context=None):</pre>
<pre class="line current"><span class="ws">        </span>cursor.execute(statement, parameters)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def do_execute_no_params(self, cursor, statement, context=None):</pre>
<pre class="line after"><span class="ws">        </span>cursor.execute(statement)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def is_disconnect(</pre></div>
</div>

<li><div class="frame" id="frame-139743861634016">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">153</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>while self.nextset():</pre>
<pre class="line before"><span class="ws">            </span>pass</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>query = self.mogrify(query, args)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>result = self._query(query)</pre>
<pre class="line after"><span class="ws">        </span>self._executed = query</pre>
<pre class="line after"><span class="ws">        </span>return result</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def executemany(self, query, args):</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Run several data against one query.</pre></div>
</div>

<li><div class="frame" id="frame-139743861634128">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">322</em>,
      in <code class="function">_query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rownumber = r</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def _query(self, q):</pre>
<pre class="line before"><span class="ws">        </span>conn = self._get_db()</pre>
<pre class="line before"><span class="ws">        </span>self._clear_result()</pre>
<pre class="line current"><span class="ws">        </span>conn.query(q)</pre>
<pre class="line after"><span class="ws">        </span>self._do_get_result()</pre>
<pre class="line after"><span class="ws">        </span>return self.rowcount</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _clear_result(self):</pre>
<pre class="line after"><span class="ws">        </span>self.rownumber = 0</pre></div>
</div>

<li><div class="frame" id="frame-139743861634240">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">558</em>,
      in <code class="function">query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># if DEBUG:</pre>
<pre class="line before"><span class="ws">        </span>#     print(&#34;DEBUG: sending query:&#34;, sql)</pre>
<pre class="line before"><span class="ws">        </span>if isinstance(sql, str):</pre>
<pre class="line before"><span class="ws">            </span>sql = sql.encode(self.encoding, &#34;surrogateescape&#34;)</pre>
<pre class="line before"><span class="ws">        </span>self._execute_command(COMMAND.COM_QUERY, sql)</pre>
<pre class="line current"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def next_result(self, unbuffered=False):</pre>
<pre class="line after"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre></div>
</div>

<li><div class="frame" id="frame-139743861634352">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">822</em>,
      in <code class="function">_read_query_result</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>result.unbuffered_active = False</pre>
<pre class="line before"><span class="ws">                </span>result.connection = None</pre>
<pre class="line before"><span class="ws">                </span>raise</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line before"><span class="ws">            </span>result = MySQLResult(self)</pre>
<pre class="line current"><span class="ws">            </span>result.read()</pre>
<pre class="line after"><span class="ws">        </span>self._result = result</pre>
<pre class="line after"><span class="ws">        </span>if result.server_status is not None:</pre>
<pre class="line after"><span class="ws">            </span>self.server_status = result.server_status</pre>
<pre class="line after"><span class="ws">        </span>return result.affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861634464">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">1200</em>,
      in <code class="function">read</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>if self.unbuffered_active:</pre>
<pre class="line before"><span class="ws">            </span>self._finish_unbuffered_query()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def read(self):</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line current"><span class="ws">            </span>first_packet = self.connection._read_packet()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if first_packet.is_ok_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_ok_packet(first_packet)</pre>
<pre class="line after"><span class="ws">            </span>elif first_packet.is_load_local_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_load_local_packet(first_packet)</pre></div>
</div>

<li><div class="frame" id="frame-139743861634576">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">772</em>,
      in <code class="function">_read_packet</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>packet = packet_type(bytes(buff), self.encoding)</pre>
<pre class="line before"><span class="ws">        </span>if packet.is_error_packet():</pre>
<pre class="line before"><span class="ws">            </span>if self._result is not None and self._result.unbuffered_active is True:</pre>
<pre class="line before"><span class="ws">                </span>self._result.unbuffered_active = False</pre>
<pre class="line current"><span class="ws">            </span>packet.raise_for_error()</pre>
<pre class="line after"><span class="ws">        </span>return packet</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _read_bytes(self, num_bytes):</pre>
<pre class="line after"><span class="ws">        </span>self._sock.settimeout(self._read_timeout)</pre>
<pre class="line after"><span class="ws">        </span>while True:</pre></div>
</div>

<li><div class="frame" id="frame-139743861634688">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py"</cite>,
      line <em class="line">221</em>,
      in <code class="function">raise_for_error</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rewind()</pre>
<pre class="line before"><span class="ws">        </span>self.advance(1)  # field_count == error (we already know that)</pre>
<pre class="line before"><span class="ws">        </span>errno = self.read_uint16()</pre>
<pre class="line before"><span class="ws">        </span>if DEBUG:</pre>
<pre class="line before"><span class="ws">            </span>print(&#34;errno =&#34;, errno)</pre>
<pre class="line current"><span class="ws">        </span>err.raise_mysql_exception(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def dump(self):</pre>
<pre class="line after"><span class="ws">        </span>dump_packet(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861634800">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py"</cite>,
      line <em class="line">143</em>,
      in <code class="function">raise_mysql_exception</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>errno = struct.unpack(&#34;&lt;h&#34;, data[1:3])[0]</pre>
<pre class="line before"><span class="ws">    </span>errval = data[9:].decode(&#34;utf-8&#34;, &#34;replace&#34;)</pre>
<pre class="line before"><span class="ws">    </span>errorclass = error_map.get(errno)</pre>
<pre class="line before"><span class="ws">    </span>if errorclass is None:</pre>
<pre class="line before"><span class="ws">        </span>errorclass = InternalError if errno &lt; 1000 else OperationalError</pre>
<pre class="line current"><span class="ws">    </span>raise errorclass(errno, errval)</pre></div>
</div>

<li><div class="exc-divider">The above exception was the direct cause of the following exception:</div>
<li><div class="frame" id="frame-139743951943520">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2213</em>,
      in <code class="function">__call__</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>def __call__(self, environ: dict, start_response: t.Callable) -&gt; t.Any:</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;The WSGI server calls the Flask application object as the</pre>
<pre class="line before"><span class="ws">        </span>WSGI application. This calls :meth:`wsgi_app`, which can be</pre>
<pre class="line before"><span class="ws">        </span>wrapped to apply middleware.</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line current"><span class="ws">        </span>return self.wsgi_app(environ, start_response)</pre></div>
</div>

<li><div class="frame" id="frame-139743952549840">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2193</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line before"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line before"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line before"><span class="ws">                </span>error = e</pre>
<pre class="line current"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>return response(environ, start_response)</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre></div>
</div>

<li><div class="frame" id="frame-139743952535952">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py"</cite>,
      line <em class="line">176</em>,
      in <code class="function">wrapped_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># Wrap exception handlers with cross_origin</pre>
<pre class="line before"><span class="ws">        </span># These error handlers will still respect the behavior of the route</pre>
<pre class="line before"><span class="ws">        </span>if options.get(&#39;intercept_exceptions&#39;, True):</pre>
<pre class="line before"><span class="ws">            </span>def _after_request_decorator(f):</pre>
<pre class="line before"><span class="ws">                </span>def wrapped_function(*args, **kwargs):</pre>
<pre class="line current"><span class="ws">                    </span>return cors_after_request(app.make_response(f(*args, **kwargs)))</pre>
<pre class="line after"><span class="ws">                </span>return wrapped_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if hasattr(app, &#39;handle_exception&#39;):</pre>
<pre class="line after"><span class="ws">                </span>app.handle_exception = _after_request_decorator(</pre>
<pre class="line after"><span class="ws">                    </span>app.handle_exception)</pre></div>
</div>

<li><div class="frame" id="frame-139743950613280">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2190</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>ctx = self.request_context(environ)</pre>
<pre class="line before"><span class="ws">        </span>error: BaseException | None = None</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line current"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line after"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">                </span>error = e</pre>
<pre class="line after"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre></div>
</div>

<li><div class="frame" id="frame-139743950616304">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1486</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line before"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line before"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line current"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>rv: ft.ResponseReturnValue | HTTPException,</pre></div>
</div>

<li><div class="frame" id="frame-139743950614848">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py"</cite>,
      line <em class="line">176</em>,
      in <code class="function">wrapped_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># Wrap exception handlers with cross_origin</pre>
<pre class="line before"><span class="ws">        </span># These error handlers will still respect the behavior of the route</pre>
<pre class="line before"><span class="ws">        </span>if options.get(&#39;intercept_exceptions&#39;, True):</pre>
<pre class="line before"><span class="ws">            </span>def _after_request_decorator(f):</pre>
<pre class="line before"><span class="ws">                </span>def wrapped_function(*args, **kwargs):</pre>
<pre class="line current"><span class="ws">                    </span>return cors_after_request(app.make_response(f(*args, **kwargs)))</pre>
<pre class="line after"><span class="ws">                </span>return wrapped_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if hasattr(app, &#39;handle_exception&#39;):</pre>
<pre class="line after"><span class="ws">                </span>app.handle_exception = _after_request_decorator(</pre>
<pre class="line after"><span class="ws">                    </span>app.handle_exception)</pre></div>
</div>

<li><div class="frame" id="frame-139743950617200">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1484</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line current"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line after"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre></div>
</div>

<li><div class="frame" id="frame-139743950617648">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1469</em>,
      in <code class="function">dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>and req.method == &#34;OPTIONS&#34;</pre>
<pre class="line before"><span class="ws">        </span>):</pre>
<pre class="line before"><span class="ws">            </span>return self.make_default_options_response()</pre>
<pre class="line before"><span class="ws">        </span># otherwise dispatch to the handler for that endpoint</pre>
<pre class="line before"><span class="ws">        </span>view_args: dict[str, t.Any] = req.view_args  # type: ignore[assignment]</pre>
<pre class="line current"><span class="ws">        </span>return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def full_dispatch_request(self) -&gt; Response:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Dispatches the request and on top of that performs request</pre>
<pre class="line after"><span class="ws">        </span>pre and postprocessing as well as HTTP exception catching and</pre>
<pre class="line after"><span class="ws">        </span>error handling.</pre></div>
</div>

<li><div class="frame" id="frame-139743950604880">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py"</cite>,
      line <em class="line">174</em>,
      in <code class="function">decorator</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>@wraps(fn)</pre>
<pre class="line before"><span class="ws">        </span>def decorator(*args, **kwargs):</pre>
<pre class="line before"><span class="ws">            </span>verify_jwt_in_request(</pre>
<pre class="line before"><span class="ws">                </span>optional, fresh, refresh, locations, verify_type, skip_revocation_check</pre>
<pre class="line before"><span class="ws">            </span>)</pre>
<pre class="line current"><span class="ws">            </span>return current_app.ensure_sync(fn)(*args, **kwargs)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>return decorator</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>return wrapper</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743863674848">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/utils/auth.py"</cite>,
      line <em class="line">23</em>,
      in <code class="function">decorated_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>return jsonify({&#39;message&#39;: &#39;Authentication required&#39;}), 401</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span># 将用户对象存储在 g 中，以便在视图函数中访问</pre>
<pre class="line before"><span class="ws">        </span>g.user = user</pre>
<pre class="line before"><span class="ws">        </span>g.user_id = user.id</pre>
<pre class="line current"><span class="ws">        </span>return f(*args, **kwargs)</pre>
<pre class="line after"><span class="ws">    </span>return decorated_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span>def role_required(role):</pre>
<pre class="line after"><span class="ws">    </span>&#34;&#34;&#34;</pre>
<pre class="line after"><span class="ws">    </span>通用的角色检查装饰器，可用于任何角色</pre></div>
</div>

<li><div class="frame" id="frame-139743863674400">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/utils/auth.py"</cite>,
      line <em class="line">43</em>,
      in <code class="function">decorated_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span># 使用 PermissionService 检查角色</pre>
<pre class="line before"><span class="ws">            </span>if not PermissionService.has_role(user_id, role):</pre>
<pre class="line before"><span class="ws">                </span>return jsonify({&#39;message&#39;: f&#39;{role.capitalize()} privileges required&#39;}), 403</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">            </span>return f(*args, **kwargs)</pre>
<pre class="line after"><span class="ws">        </span>return decorated_function</pre>
<pre class="line after"><span class="ws">    </span>return decorator</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span># 为常用角色提供便捷装饰器</pre>
<pre class="line after"><span class="ws"></span>def admin_required(f):</pre></div>
</div>

<li><div class="frame" id="frame-139743863674176">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/api/admin.py"</cite>,
      line <em class="line">76</em>,
      in <code class="function">manage_user</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>except ValueError:</pre>
<pre class="line before"><span class="ws">            </span>return jsonify({</pre>
<pre class="line before"><span class="ws">                </span>&#39;error&#39;: &#39;Invalid duration&#39;</pre>
<pre class="line before"><span class="ws">            </span>}), 400</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">    </span>result = AdminService.manage_user(</pre>
<pre class="line after"><span class="ws">        </span>admin_id=admin_id,</pre>
<pre class="line after"><span class="ws">        </span>user_id=user_id,</pre>
<pre class="line after"><span class="ws">        </span>action=action,</pre>
<pre class="line after"><span class="ws">        </span>reason=reason,</pre>
<pre class="line after"><span class="ws">        </span>duration=duration</pre></div>
</div>

<li><div class="frame" id="frame-139743863680336">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/services/admin_service.py"</cite>,
      line <em class="line">59</em>,
      in <code class="function">manage_user</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>Returns:</pre>
<pre class="line before"><span class="ws">            </span>Action result</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>if action == &#39;ban&#39;:</pre>
<pre class="line current"><span class="ws">            </span>user_action = AdminDAO.ban_user(admin_id, user_id, reason, duration)</pre>
<pre class="line after"><span class="ws">            </span>return {</pre>
<pre class="line after"><span class="ws">                </span>&#39;success&#39;: True,</pre>
<pre class="line after"><span class="ws">                </span>&#39;message&#39;: f&#34;User {user_id} has been banned&#34;,</pre>
<pre class="line after"><span class="ws">                </span>&#39;action_id&#39;: user_action.id</pre>
<pre class="line after"><span class="ws">            </span>}</pre></div>
</div>

<li><div class="frame" id="frame-139743863588336">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/dao/admin_dao.py"</cite>,
      line <em class="line">96</em>,
      in <code class="function">ban_user</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>reason=reason,</pre>
<pre class="line before"><span class="ws">            </span>duration=duration</pre>
<pre class="line before"><span class="ws">        </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>db.session.add(action)</pre>
<pre class="line current"><span class="ws">        </span>db.session.commit()</pre>
<pre class="line after"><span class="ws">        </span>return action</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>@staticmethod</pre>
<pre class="line after"><span class="ws">    </span>def unban_user(admin_id: int, user_id: int, reason: str) -&gt; UserAction:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;</pre></div>
</div>

<li><div class="frame" id="frame-139743863593376">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/scoping.py"</cite>,
      line <em class="line">599</em>,
      in <code class="function">commit</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>:ref:`asyncio_orm_avoid_lazyloads`</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;  # noqa: E501</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>return self._proxied.commit()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def connection(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>bind_arguments: Optional[_BindArguments] = None,</pre>
<pre class="line after"><span class="ws">        </span>execution_options: Optional[CoreExecuteOptionsParameter] = None,</pre></div>
</div>

<li><div class="frame" id="frame-139743863939120">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">2032</em>,
      in <code class="function">commit</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>trans = self._transaction</pre>
<pre class="line before"><span class="ws">        </span>if trans is None:</pre>
<pre class="line before"><span class="ws">            </span>trans = self._autobegin_t()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>trans.commit(_to_root=True)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def prepare(self) -&gt; None:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Prepare the current transaction in progress for two phase commit.</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>If no transaction is in progress, this method raises an</pre></div>
</div>

<li><div class="frame" id="frame-139743862278960">
  <h4>File <cite class="filename">"&lt;string&gt;"</cite>,
      line <em class="line">2</em>,
      in <code class="function">commit</code></h4>
  <div class="source "></div>
</div>

<li><div class="frame" id="frame-139743862279072">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py"</cite>,
      line <em class="line">139</em>,
      in <code class="function">_go</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                    </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>self._current_fn = fn</pre>
<pre class="line before"><span class="ws">            </span>self._next_state = _StateChangeStates.CHANGE_IN_PROGRESS</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>ret_value = fn(self, *arg, **kw)</pre>
<pre class="line after"><span class="ws">            </span>except:</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>if self._state is expect_state:</pre>
<pre class="line after"><span class="ws">                    </span>return ret_value</pre></div>
</div>

<li><div class="frame" id="frame-139743862282880">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">1313</em>,
      in <code class="function">commit</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>SessionTransactionState.CLOSED,</pre>
<pre class="line before"><span class="ws">    </span>)</pre>
<pre class="line before"><span class="ws">    </span>def commit(self, _to_root: bool = False) -&gt; None:</pre>
<pre class="line before"><span class="ws">        </span>if self._state is not SessionTransactionState.PREPARED:</pre>
<pre class="line before"><span class="ws">            </span>with self._expect_state(SessionTransactionState.PREPARED):</pre>
<pre class="line current"><span class="ws">                </span>self._prepare_impl()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>if self._parent is None or self.nested:</pre>
<pre class="line after"><span class="ws">            </span>for conn, trans, should_commit, autoclose in set(</pre>
<pre class="line after"><span class="ws">                </span>self._connections.values()</pre>
<pre class="line after"><span class="ws">            </span>):</pre></div>
</div>

<li><div class="frame" id="frame-139743862282992">
  <h4>File <cite class="filename">"&lt;string&gt;"</cite>,
      line <em class="line">2</em>,
      in <code class="function">_prepare_impl</code></h4>
  <div class="source "></div>
</div>

<li><div class="frame" id="frame-139743862283104">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py"</cite>,
      line <em class="line">139</em>,
      in <code class="function">_go</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                    </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>self._current_fn = fn</pre>
<pre class="line before"><span class="ws">            </span>self._next_state = _StateChangeStates.CHANGE_IN_PROGRESS</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>ret_value = fn(self, *arg, **kw)</pre>
<pre class="line after"><span class="ws">            </span>except:</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>if self._state is expect_state:</pre>
<pre class="line after"><span class="ws">                    </span>return ret_value</pre></div>
</div>

<li><div class="frame" id="frame-139743862283216">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">1288</em>,
      in <code class="function">_prepare_impl</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if not self.session._flushing:</pre>
<pre class="line before"><span class="ws">            </span>for _flush_guard in range(100):</pre>
<pre class="line before"><span class="ws">                </span>if self.session._is_clean():</pre>
<pre class="line before"><span class="ws">                    </span>break</pre>
<pre class="line current"><span class="ws">                </span>self.session.flush()</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>raise exc.FlushError(</pre>
<pre class="line after"><span class="ws">                    </span>&#34;Over 100 subsequent flushes have occurred within &#34;</pre>
<pre class="line after"><span class="ws">                    </span>&#34;session.commit() - is an after_flush() hook &#34;</pre>
<pre class="line after"><span class="ws">                    </span>&#34;creating new objects?&#34;</pre></div>
</div>

<li><div class="frame" id="frame-139743862283328">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">4353</em>,
      in <code class="function">flush</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if self._is_clean():</pre>
<pre class="line before"><span class="ws">            </span>return</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>self._flushing = True</pre>
<pre class="line current"><span class="ws">            </span>self._flush(objects)</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre>
<pre class="line after"><span class="ws">            </span>self._flushing = False</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _flush_warning(self, method: Any) -&gt; None:</pre>
<pre class="line after"><span class="ws">        </span>util.warn(</pre></div>
</div>

<li><div class="frame" id="frame-139743862283440">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">4488</em>,
      in <code class="function">_flush</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>self.dispatch.after_flush_postexec(self, flush_context)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>transaction.commit()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>except:</pre>
<pre class="line current"><span class="ws">            </span>with util.safe_reraise():</pre>
<pre class="line after"><span class="ws">                </span>transaction.rollback(_capture_exception=True)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def bulk_save_objects(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>objects: Iterable[object],</pre></div>
</div>

<li><div class="frame" id="frame-139743862283552">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py"</cite>,
      line <em class="line">146</em>,
      in <code class="function">__exit__</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># see #2703 for notes</pre>
<pre class="line before"><span class="ws">        </span>if type_ is None:</pre>
<pre class="line before"><span class="ws">            </span>exc_type, exc_value, exc_tb = self._exc_info</pre>
<pre class="line before"><span class="ws">            </span>assert exc_value is not None</pre>
<pre class="line before"><span class="ws">            </span>self._exc_info = None  # remove potential circular references</pre>
<pre class="line current"><span class="ws">            </span>raise exc_value.with_traceback(exc_tb)</pre>
<pre class="line after"><span class="ws">        </span>else:</pre>
<pre class="line after"><span class="ws">            </span>self._exc_info = None  # remove potential circular references</pre>
<pre class="line after"><span class="ws">            </span>assert value is not None</pre>
<pre class="line after"><span class="ws">            </span>raise value.with_traceback(traceback)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743862474784">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">4449</em>,
      in <code class="function">_flush</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>flush_context.transaction = transaction = self._autobegin_t()._begin()</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>self._warn_on_events = True</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>flush_context.execute()</pre>
<pre class="line after"><span class="ws">            </span>finally:</pre>
<pre class="line after"><span class="ws">                </span>self._warn_on_events = False</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>self.dispatch.after_flush(self, flush_context)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743862474896">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py"</cite>,
      line <em class="line">466</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>while set_:</pre>
<pre class="line before"><span class="ws">                    </span>n = set_.pop()</pre>
<pre class="line before"><span class="ws">                    </span>n.execute_aggregate(self, set_)</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line before"><span class="ws">            </span>for rec in topological.sort(self.dependencies, postsort_actions):</pre>
<pre class="line current"><span class="ws">                </span>rec.execute(self)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_flush_changes(self) -&gt; None:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Mark processed objects as clean / deleted after a successful</pre>
<pre class="line after"><span class="ws">        </span>flush().</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743862540432">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py"</cite>,
      line <em class="line">642</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.sort_key = (&#34;SaveUpdateAll&#34;, mapper._sort_key)</pre>
<pre class="line before"><span class="ws">        </span>assert mapper is mapper.base_mapper</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>@util.preload_module(&#34;sqlalchemy.orm.persistence&#34;)</pre>
<pre class="line before"><span class="ws">    </span>def execute(self, uow):</pre>
<pre class="line current"><span class="ws">        </span>util.preloaded.orm_persistence.save_obj(</pre>
<pre class="line after"><span class="ws">            </span>self.mapper,</pre>
<pre class="line after"><span class="ws">            </span>uow.states_for_mapper_hierarchy(self.mapper, False, False),</pre>
<pre class="line after"><span class="ws">            </span>uow,</pre>
<pre class="line after"><span class="ws">        </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743862540544">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py"</cite>,
      line <em class="line">93</em>,
      in <code class="function">save_obj</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>mapper,</pre>
<pre class="line before"><span class="ws">            </span>table,</pre>
<pre class="line before"><span class="ws">            </span>update,</pre>
<pre class="line before"><span class="ws">        </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>_emit_insert_statements(</pre>
<pre class="line after"><span class="ws">            </span>base_mapper,</pre>
<pre class="line after"><span class="ws">            </span>uowtransaction,</pre>
<pre class="line after"><span class="ws">            </span>mapper,</pre>
<pre class="line after"><span class="ws">            </span>table,</pre>
<pre class="line after"><span class="ws">            </span>insert,</pre></div>
</div>

<li><div class="frame" id="frame-139743862650720">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py"</cite>,
      line <em class="line">1233</em>,
      in <code class="function">_emit_insert_statements</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                            </span>statement.values(value_params),</pre>
<pre class="line before"><span class="ws">                            </span>params,</pre>
<pre class="line before"><span class="ws">                            </span>execution_options=execution_options,</pre>
<pre class="line before"><span class="ws">                        </span>)</pre>
<pre class="line before"><span class="ws">                    </span>else:</pre>
<pre class="line current"><span class="ws">                        </span>result = connection.execute(</pre>
<pre class="line after"><span class="ws">                            </span>statement,</pre>
<pre class="line after"><span class="ws">                            </span>params,</pre>
<pre class="line after"><span class="ws">                            </span>execution_options=execution_options,</pre>
<pre class="line after"><span class="ws">                        </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743862650832">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1416</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>meth = statement._execute_on_connection</pre>
<pre class="line before"><span class="ws">        </span>except AttributeError as err:</pre>
<pre class="line before"><span class="ws">            </span>raise exc.ObjectNotExecutableError(statement) from err</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line current"><span class="ws">            </span>return meth(</pre>
<pre class="line after"><span class="ws">                </span>self,</pre>
<pre class="line after"><span class="ws">                </span>distilled_parameters,</pre>
<pre class="line after"><span class="ws">                </span>execution_options or NO_OPTIONS,</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743862924992">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/sql/elements.py"</cite>,
      line <em class="line">523</em>,
      in <code class="function">_execute_on_connection</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>execution_options: CoreExecuteOptionsParameter,</pre>
<pre class="line before"><span class="ws">    </span>) -&gt; Result[Any]:</pre>
<pre class="line before"><span class="ws">        </span>if self.supports_execution:</pre>
<pre class="line before"><span class="ws">            </span>if TYPE_CHECKING:</pre>
<pre class="line before"><span class="ws">                </span>assert isinstance(self, Executable)</pre>
<pre class="line current"><span class="ws">            </span>return connection._execute_clauseelement(</pre>
<pre class="line after"><span class="ws">                </span>self, distilled_params, execution_options</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws">        </span>else:</pre>
<pre class="line after"><span class="ws">            </span>raise exc.ObjectNotExecutableError(self)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861253936">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1638</em>,
      in <code class="function">_execute_clauseelement</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>column_keys=keys,</pre>
<pre class="line before"><span class="ws">            </span>for_executemany=for_executemany,</pre>
<pre class="line before"><span class="ws">            </span>schema_translate_map=schema_translate_map,</pre>
<pre class="line before"><span class="ws">            </span>linting=self.dialect.compiler_linting | compiler.WARN_LINTING,</pre>
<pre class="line before"><span class="ws">        </span>)</pre>
<pre class="line current"><span class="ws">        </span>ret = self._execute_context(</pre>
<pre class="line after"><span class="ws">            </span>dialect,</pre>
<pre class="line after"><span class="ws">            </span>dialect.execution_ctx_cls._init_compiled,</pre>
<pre class="line after"><span class="ws">            </span>compiled_sql,</pre>
<pre class="line after"><span class="ws">            </span>distilled_parameters,</pre>
<pre class="line after"><span class="ws">            </span>execution_options,</pre></div>
</div>

<li><div class="frame" id="frame-139743861254048">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1843</em>,
      in <code class="function">_execute_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>context.pre_exec()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if context.execute_style is ExecuteStyle.INSERTMANYVALUES:</pre>
<pre class="line before"><span class="ws">            </span>return self._exec_insertmany_context(dialect, context)</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line current"><span class="ws">            </span>return self._exec_single_context(</pre>
<pre class="line after"><span class="ws">                </span>dialect, context, statement, parameters</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _exec_single_context(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre></div>
</div>

<li><div class="frame" id="frame-139743861254160">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1983</em>,
      in <code class="function">_exec_single_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>context.post_exec()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>result = context._setup_result_proxy()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>except BaseException as e:</pre>
<pre class="line current"><span class="ws">            </span>self._handle_dbapi_exception(</pre>
<pre class="line after"><span class="ws">                </span>e, str_statement, effective_parameters, cursor, context</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>return result</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861254272">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">2352</em>,
      in <code class="function">_handle_dbapi_exception</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>if newraise:</pre>
<pre class="line before"><span class="ws">                </span>raise newraise.with_traceback(exc_info[2]) from e</pre>
<pre class="line before"><span class="ws">            </span>elif should_wrap:</pre>
<pre class="line before"><span class="ws">                </span>assert sqlalchemy_exception is not None</pre>
<pre class="line current"><span class="ws">                </span>raise sqlalchemy_exception.with_traceback(exc_info[2]) from e</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>assert exc_info[1] is not None</pre>
<pre class="line after"><span class="ws">                </span>raise exc_info[1].with_traceback(exc_info[2])</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre>
<pre class="line after"><span class="ws">            </span>del self._reentrant_error</pre></div>
</div>

<li><div class="frame" id="frame-139743861254384">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1964</em>,
      in <code class="function">_exec_single_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                            </span>context,</pre>
<pre class="line before"><span class="ws">                        </span>):</pre>
<pre class="line before"><span class="ws">                            </span>evt_handled = True</pre>
<pre class="line before"><span class="ws">                            </span>break</pre>
<pre class="line before"><span class="ws">                </span>if not evt_handled:</pre>
<pre class="line current"><span class="ws">                    </span>self.dialect.do_execute(</pre>
<pre class="line after"><span class="ws">                        </span>cursor, str_statement, effective_parameters, context</pre>
<pre class="line after"><span class="ws">                    </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if self._has_events or self.engine._has_events:</pre>
<pre class="line after"><span class="ws">                </span>self.dispatch.after_cursor_execute(</pre></div>
</div>

<li><div class="frame" id="frame-139743861254496">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py"</cite>,
      line <em class="line">945</em>,
      in <code class="function">do_execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_executemany(self, cursor, statement, parameters, context=None):</pre>
<pre class="line before"><span class="ws">        </span>cursor.executemany(statement, parameters)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_execute(self, cursor, statement, parameters, context=None):</pre>
<pre class="line current"><span class="ws">        </span>cursor.execute(statement, parameters)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def do_execute_no_params(self, cursor, statement, context=None):</pre>
<pre class="line after"><span class="ws">        </span>cursor.execute(statement)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def is_disconnect(</pre></div>
</div>

<li><div class="frame" id="frame-139743861465920">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">153</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>while self.nextset():</pre>
<pre class="line before"><span class="ws">            </span>pass</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>query = self.mogrify(query, args)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>result = self._query(query)</pre>
<pre class="line after"><span class="ws">        </span>self._executed = query</pre>
<pre class="line after"><span class="ws">        </span>return result</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def executemany(self, query, args):</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Run several data against one query.</pre></div>
</div>

<li><div class="frame" id="frame-139743861470512">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">322</em>,
      in <code class="function">_query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rownumber = r</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def _query(self, q):</pre>
<pre class="line before"><span class="ws">        </span>conn = self._get_db()</pre>
<pre class="line before"><span class="ws">        </span>self._clear_result()</pre>
<pre class="line current"><span class="ws">        </span>conn.query(q)</pre>
<pre class="line after"><span class="ws">        </span>self._do_get_result()</pre>
<pre class="line after"><span class="ws">        </span>return self.rowcount</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _clear_result(self):</pre>
<pre class="line after"><span class="ws">        </span>self.rownumber = 0</pre></div>
</div>

<li><div class="frame" id="frame-139743861470624">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">558</em>,
      in <code class="function">query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># if DEBUG:</pre>
<pre class="line before"><span class="ws">        </span>#     print(&#34;DEBUG: sending query:&#34;, sql)</pre>
<pre class="line before"><span class="ws">        </span>if isinstance(sql, str):</pre>
<pre class="line before"><span class="ws">            </span>sql = sql.encode(self.encoding, &#34;surrogateescape&#34;)</pre>
<pre class="line before"><span class="ws">        </span>self._execute_command(COMMAND.COM_QUERY, sql)</pre>
<pre class="line current"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def next_result(self, unbuffered=False):</pre>
<pre class="line after"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre></div>
</div>

<li><div class="frame" id="frame-139743861628752">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">822</em>,
      in <code class="function">_read_query_result</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>result.unbuffered_active = False</pre>
<pre class="line before"><span class="ws">                </span>result.connection = None</pre>
<pre class="line before"><span class="ws">                </span>raise</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line before"><span class="ws">            </span>result = MySQLResult(self)</pre>
<pre class="line current"><span class="ws">            </span>result.read()</pre>
<pre class="line after"><span class="ws">        </span>self._result = result</pre>
<pre class="line after"><span class="ws">        </span>if result.server_status is not None:</pre>
<pre class="line after"><span class="ws">            </span>self.server_status = result.server_status</pre>
<pre class="line after"><span class="ws">        </span>return result.affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861628864">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">1200</em>,
      in <code class="function">read</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>if self.unbuffered_active:</pre>
<pre class="line before"><span class="ws">            </span>self._finish_unbuffered_query()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def read(self):</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line current"><span class="ws">            </span>first_packet = self.connection._read_packet()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if first_packet.is_ok_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_ok_packet(first_packet)</pre>
<pre class="line after"><span class="ws">            </span>elif first_packet.is_load_local_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_load_local_packet(first_packet)</pre></div>
</div>

<li><div class="frame" id="frame-139743861628976">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">772</em>,
      in <code class="function">_read_packet</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>packet = packet_type(bytes(buff), self.encoding)</pre>
<pre class="line before"><span class="ws">        </span>if packet.is_error_packet():</pre>
<pre class="line before"><span class="ws">            </span>if self._result is not None and self._result.unbuffered_active is True:</pre>
<pre class="line before"><span class="ws">                </span>self._result.unbuffered_active = False</pre>
<pre class="line current"><span class="ws">            </span>packet.raise_for_error()</pre>
<pre class="line after"><span class="ws">        </span>return packet</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _read_bytes(self, num_bytes):</pre>
<pre class="line after"><span class="ws">        </span>self._sock.settimeout(self._read_timeout)</pre>
<pre class="line after"><span class="ws">        </span>while True:</pre></div>
</div>

<li><div class="frame" id="frame-139743861629088">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py"</cite>,
      line <em class="line">221</em>,
      in <code class="function">raise_for_error</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rewind()</pre>
<pre class="line before"><span class="ws">        </span>self.advance(1)  # field_count == error (we already know that)</pre>
<pre class="line before"><span class="ws">        </span>errno = self.read_uint16()</pre>
<pre class="line before"><span class="ws">        </span>if DEBUG:</pre>
<pre class="line before"><span class="ws">            </span>print(&#34;errno =&#34;, errno)</pre>
<pre class="line current"><span class="ws">        </span>err.raise_mysql_exception(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def dump(self):</pre>
<pre class="line after"><span class="ws">        </span>dump_packet(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861633120">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py"</cite>,
      line <em class="line">143</em>,
      in <code class="function">raise_mysql_exception</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>errno = struct.unpack(&#34;&lt;h&#34;, data[1:3])[0]</pre>
<pre class="line before"><span class="ws">    </span>errval = data[9:].decode(&#34;utf-8&#34;, &#34;replace&#34;)</pre>
<pre class="line before"><span class="ws">    </span>errorclass = error_map.get(errno)</pre>
<pre class="line before"><span class="ws">    </span>if errorclass is None:</pre>
<pre class="line before"><span class="ws">        </span>errorclass = InternalError if errno &lt; 1000 else OperationalError</pre>
<pre class="line current"><span class="ws">    </span>raise errorclass(errno, errval)</pre></div>
</div>
</ul>
  <blockquote>sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1452, &#39;Cannot add or update a child row: a foreign key constraint fails (`novel_db`.`user_action`, CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`))&#39;)
[SQL: INSERT INTO user_action (admin_id, target_user_id, action_type, reason, duration, created_at) VALUES (%(admin_id)s, %(target_user_id)s, %(action_type)s, %(reason)s, %(duration)s, %(created_at)s)]
[parameters: {&#39;admin_id&#39;: 6, &#39;target_user_id&#39;: 42, &#39;action_type&#39;: &#39;ban&#39;, &#39;reason&#39;: &#39;测试禁用功能&#39;, &#39;duration&#39;: 1, &#39;created_at&#39;: datetime.datetime(2025, 4, 24, 2, 23, 33, 351796)}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
</blockquote>
</div>

<div class="plain">
    <p>
      This is the Copy/Paste friendly version of the traceback.
    </p>
    <textarea cols="50" rows="10" name="code" readonly>Traceback (most recent call last):
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1964, in _exec_single_context
    self.dialect.do_execute(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py&#34;, line 945, in do_execute
    cursor.execute(statement, parameters)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 153, in execute
    result = self._query(query)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 322, in _query
    conn.query(q)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 822, in _read_query_result
    result.read()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 1200, in read
    first_packet = self.connection._read_packet()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 772, in _read_packet
    packet.raise_for_error()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py&#34;, line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py&#34;, line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.IntegrityError: (1452, &#39;Cannot add or update a child row: a foreign key constraint fails (`novel_db`.`user_action`, CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`))&#39;)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2213, in __call__
    return self.wsgi_app(environ, start_response)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2193, in wsgi_app
    response = self.handle_exception(e)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py&#34;, line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py&#34;, line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py&#34;, line 174, in decorator
    return current_app.ensure_sync(fn)(*args, **kwargs)
  File &#34;/home/chris/novels/backend/app/utils/auth.py&#34;, line 23, in decorated_function
    return f(*args, **kwargs)
  File &#34;/home/chris/novels/backend/app/utils/auth.py&#34;, line 43, in decorated_function
    return f(*args, **kwargs)
  File &#34;/home/chris/novels/backend/app/api/admin.py&#34;, line 76, in manage_user
    result = AdminService.manage_user(
  File &#34;/home/chris/novels/backend/app/services/admin_service.py&#34;, line 59, in manage_user
    user_action = AdminDAO.ban_user(admin_id, user_id, reason, duration)
  File &#34;/home/chris/novels/backend/app/dao/admin_dao.py&#34;, line 96, in ban_user
    db.session.commit()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/scoping.py&#34;, line 599, in commit
    return self._proxied.commit()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 2032, in commit
    trans.commit(_to_root=True)
  File &#34;&lt;string&gt;&#34;, line 2, in commit
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py&#34;, line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 1313, in commit
    self._prepare_impl()
  File &#34;&lt;string&gt;&#34;, line 2, in _prepare_impl
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py&#34;, line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 1288, in _prepare_impl
    self.session.flush()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 4353, in flush
    self._flush(objects)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 4488, in _flush
    with util.safe_reraise():
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py&#34;, line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 4449, in _flush
    flush_context.execute()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py&#34;, line 466, in execute
    rec.execute(self)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py&#34;, line 642, in execute
    util.preloaded.orm_persistence.save_obj(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py&#34;, line 93, in save_obj
    _emit_insert_statements(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py&#34;, line 1233, in _emit_insert_statements
    result = connection.execute(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1416, in execute
    return meth(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/sql/elements.py&#34;, line 523, in _execute_on_connection
    return connection._execute_clauseelement(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1638, in _execute_clauseelement
    ret = self._execute_context(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1843, in _execute_context
    return self._exec_single_context(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1983, in _exec_single_context
    self._handle_dbapi_exception(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 2352, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1964, in _exec_single_context
    self.dialect.do_execute(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py&#34;, line 945, in do_execute
    cursor.execute(statement, parameters)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 153, in execute
    result = self._query(query)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 322, in _query
    conn.query(q)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 822, in _read_query_result
    result.read()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 1200, in read
    first_packet = self.connection._read_packet()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 772, in _read_packet
    packet.raise_for_error()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py&#34;, line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py&#34;, line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1452, &#39;Cannot add or update a child row: a foreign key constraint fails (`novel_db`.`user_action`, CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`))&#39;)
[SQL: INSERT INTO user_action (admin_id, target_user_id, action_type, reason, duration, created_at) VALUES (%(admin_id)s, %(target_user_id)s, %(action_type)s, %(reason)s, %(duration)s, %(created_at)s)]
[parameters: {&#39;admin_id&#39;: 6, &#39;target_user_id&#39;: 42, &#39;action_type&#39;: &#39;ban&#39;, &#39;reason&#39;: &#39;测试禁用功能&#39;, &#39;duration&#39;: 1, &#39;created_at&#39;: datetime.datetime(2025, 4, 24, 2, 23, 33, 351796)}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
</textarea>
</div>
<div class="explanation">
  The debugger caught an exception in your WSGI application.  You can now
  look at the traceback which led to the error.  <span class="nojavascript">
  If you enable JavaScript you can also use additional features such as code
  execution (if the evalex feature is enabled), automatic pasting of the
  exceptions and much more.</span>
</div>
      <div class="footer">
        Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
        friendly Werkzeug powered traceback interpreter.
      </div>
    </div>

    <div class="pin-prompt">
      <div class="inner">
        <h3>Console Locked</h3>
        <p>
          The console is locked and needs to be unlocked by entering the PIN.
          You can find the PIN printed out on the standard output of your
          shell that runs the server.
        <form>
          <p>PIN:
            <input type=text name=pin size=14>
            <input type=submit name=btn value="Confirm Pin">
        </form>
      </div>
    </div>
  </body>
</html>

<!--

Traceback (most recent call last):
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1964, in _exec_single_context
    self.dialect.do_execute(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 945, in do_execute
    cursor.execute(statement, parameters)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 153, in execute
    result = self._query(query)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 322, in _query
    conn.query(q)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 822, in _read_query_result
    result.read()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.IntegrityError: (1452, 'Cannot add or update a child row: a foreign key constraint fails (`novel_db`.`user_action`, CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`))')

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py", line 174, in decorator
    return current_app.ensure_sync(fn)(*args, **kwargs)
  File "/home/chris/novels/backend/app/utils/auth.py", line 23, in decorated_function
    return f(*args, **kwargs)
  File "/home/chris/novels/backend/app/utils/auth.py", line 43, in decorated_function
    return f(*args, **kwargs)
  File "/home/chris/novels/backend/app/api/admin.py", line 76, in manage_user
    result = AdminService.manage_user(
  File "/home/chris/novels/backend/app/services/admin_service.py", line 59, in manage_user
    user_action = AdminDAO.ban_user(admin_id, user_id, reason, duration)
  File "/home/chris/novels/backend/app/dao/admin_dao.py", line 96, in ban_user
    db.session.commit()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/scoping.py", line 599, in commit
    return self._proxied.commit()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2032, in commit
    trans.commit(_to_root=True)
  File "<string>", line 2, in commit
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1313, in commit
    self._prepare_impl()
  File "<string>", line 2, in _prepare_impl
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1288, in _prepare_impl
    self.session.flush()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 4353, in flush
    self._flush(objects)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 4488, in _flush
    with util.safe_reraise():
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 4449, in _flush
    flush_context.execute()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py", line 466, in execute
    rec.execute(self)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py", line 93, in save_obj
    _emit_insert_statements(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py", line 1233, in _emit_insert_statements
    result = connection.execute(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1416, in execute
    return meth(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/sql/elements.py", line 523, in _execute_on_connection
    return connection._execute_clauseelement(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1638, in _execute_clauseelement
    ret = self._execute_context(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1843, in _execute_context
    return self._exec_single_context(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1983, in _exec_single_context
    self._handle_dbapi_exception(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2352, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1964, in _exec_single_context
    self.dialect.do_execute(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 945, in do_execute
    cursor.execute(statement, parameters)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 153, in execute
    result = self._query(query)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 322, in _query
    conn.query(q)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 822, in _read_query_result
    result.read()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1452, 'Cannot add or update a child row: a foreign key constraint fails (`novel_db`.`user_action`, CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`))')
[SQL: INSERT INTO user_action (admin_id, target_user_id, action_type, reason, duration, created_at) VALUES (%(admin_id)s, %(target_user_id)s, %(action_type)s, %(reason)s, %(duration)s, %(created_at)s)]
[parameters: {'admin_id': 6, 'target_user_id': 42, 'action_type': 'ban', 'reason': '测试禁用功能', 'duration': 1, 'created_at': datetime.datetime(2025, 4, 24, 2, 23, 33, 351796)}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)


-->

❌ 失败: 禁用请求失败，状态码: 500
解禁用户 42
状态码: 500
响应内容: <!doctype html>
<html lang=en>
  <head>
    <title>ValueError: User 42 is not banned
 // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css">
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script>
      var CONSOLE_MODE = false,
          EVALEX = true,
          EVALEX_TRUSTED = false,
          SECRET = "hGZxCLme2nil2UPZIPjG";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
<h1>ValueError</h1>
<div class="detail">
  <p class="errormsg">ValueError: User 42 is not banned
</p>
</div>
<h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
<div class="traceback">
  <h3></h3>
  <ul><li><div class="frame" id="frame-139743861881008">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2213</em>,
      in <code class="function">__call__</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>def __call__(self, environ: dict, start_response: t.Callable) -&gt; t.Any:</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;The WSGI server calls the Flask application object as the</pre>
<pre class="line before"><span class="ws">        </span>WSGI application. This calls :meth:`wsgi_app`, which can be</pre>
<pre class="line before"><span class="ws">        </span>wrapped to apply middleware.</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line current"><span class="ws">        </span>return self.wsgi_app(environ, start_response)</pre></div>
</div>

<li><div class="frame" id="frame-139743861881120">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2193</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line before"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line before"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line before"><span class="ws">                </span>error = e</pre>
<pre class="line current"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>return response(environ, start_response)</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre></div>
</div>

<li><div class="frame" id="frame-139743861880448">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py"</cite>,
      line <em class="line">176</em>,
      in <code class="function">wrapped_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># Wrap exception handlers with cross_origin</pre>
<pre class="line before"><span class="ws">        </span># These error handlers will still respect the behavior of the route</pre>
<pre class="line before"><span class="ws">        </span>if options.get(&#39;intercept_exceptions&#39;, True):</pre>
<pre class="line before"><span class="ws">            </span>def _after_request_decorator(f):</pre>
<pre class="line before"><span class="ws">                </span>def wrapped_function(*args, **kwargs):</pre>
<pre class="line current"><span class="ws">                    </span>return cors_after_request(app.make_response(f(*args, **kwargs)))</pre>
<pre class="line after"><span class="ws">                </span>return wrapped_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if hasattr(app, &#39;handle_exception&#39;):</pre>
<pre class="line after"><span class="ws">                </span>app.handle_exception = _after_request_decorator(</pre>
<pre class="line after"><span class="ws">                    </span>app.handle_exception)</pre></div>
</div>

<li><div class="frame" id="frame-139743861879888">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2190</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>ctx = self.request_context(environ)</pre>
<pre class="line before"><span class="ws">        </span>error: BaseException | None = None</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line current"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line after"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">                </span>error = e</pre>
<pre class="line after"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre></div>
</div>

<li><div class="frame" id="frame-139743861882128">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1486</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line before"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line before"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line current"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>rv: ft.ResponseReturnValue | HTTPException,</pre></div>
</div>

<li><div class="frame" id="frame-139743861880336">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py"</cite>,
      line <em class="line">176</em>,
      in <code class="function">wrapped_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># Wrap exception handlers with cross_origin</pre>
<pre class="line before"><span class="ws">        </span># These error handlers will still respect the behavior of the route</pre>
<pre class="line before"><span class="ws">        </span>if options.get(&#39;intercept_exceptions&#39;, True):</pre>
<pre class="line before"><span class="ws">            </span>def _after_request_decorator(f):</pre>
<pre class="line before"><span class="ws">                </span>def wrapped_function(*args, **kwargs):</pre>
<pre class="line current"><span class="ws">                    </span>return cors_after_request(app.make_response(f(*args, **kwargs)))</pre>
<pre class="line after"><span class="ws">                </span>return wrapped_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if hasattr(app, &#39;handle_exception&#39;):</pre>
<pre class="line after"><span class="ws">                </span>app.handle_exception = _after_request_decorator(</pre>
<pre class="line after"><span class="ws">                    </span>app.handle_exception)</pre></div>
</div>

<li><div class="frame" id="frame-139743861880112">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1484</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line current"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line after"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre></div>
</div>

<li><div class="frame" id="frame-139743861879776">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1469</em>,
      in <code class="function">dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>and req.method == &#34;OPTIONS&#34;</pre>
<pre class="line before"><span class="ws">        </span>):</pre>
<pre class="line before"><span class="ws">            </span>return self.make_default_options_response()</pre>
<pre class="line before"><span class="ws">        </span># otherwise dispatch to the handler for that endpoint</pre>
<pre class="line before"><span class="ws">        </span>view_args: dict[str, t.Any] = req.view_args  # type: ignore[assignment]</pre>
<pre class="line current"><span class="ws">        </span>return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def full_dispatch_request(self) -&gt; Response:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Dispatches the request and on top of that performs request</pre>
<pre class="line after"><span class="ws">        </span>pre and postprocessing as well as HTTP exception catching and</pre>
<pre class="line after"><span class="ws">        </span>error handling.</pre></div>
</div>

<li><div class="frame" id="frame-139743861879664">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py"</cite>,
      line <em class="line">174</em>,
      in <code class="function">decorator</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>@wraps(fn)</pre>
<pre class="line before"><span class="ws">        </span>def decorator(*args, **kwargs):</pre>
<pre class="line before"><span class="ws">            </span>verify_jwt_in_request(</pre>
<pre class="line before"><span class="ws">                </span>optional, fresh, refresh, locations, verify_type, skip_revocation_check</pre>
<pre class="line before"><span class="ws">            </span>)</pre>
<pre class="line current"><span class="ws">            </span>return current_app.ensure_sync(fn)(*args, **kwargs)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>return decorator</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>return wrapper</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861876976">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/utils/auth.py"</cite>,
      line <em class="line">23</em>,
      in <code class="function">decorated_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>return jsonify({&#39;message&#39;: &#39;Authentication required&#39;}), 401</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span># 将用户对象存储在 g 中，以便在视图函数中访问</pre>
<pre class="line before"><span class="ws">        </span>g.user = user</pre>
<pre class="line before"><span class="ws">        </span>g.user_id = user.id</pre>
<pre class="line current"><span class="ws">        </span>return f(*args, **kwargs)</pre>
<pre class="line after"><span class="ws">    </span>return decorated_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span>def role_required(role):</pre>
<pre class="line after"><span class="ws">    </span>&#34;&#34;&#34;</pre>
<pre class="line after"><span class="ws">    </span>通用的角色检查装饰器，可用于任何角色</pre></div>
</div>

<li><div class="frame" id="frame-139743861879552">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/utils/auth.py"</cite>,
      line <em class="line">43</em>,
      in <code class="function">decorated_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span># 使用 PermissionService 检查角色</pre>
<pre class="line before"><span class="ws">            </span>if not PermissionService.has_role(user_id, role):</pre>
<pre class="line before"><span class="ws">                </span>return jsonify({&#39;message&#39;: f&#39;{role.capitalize()} privileges required&#39;}), 403</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">            </span>return f(*args, **kwargs)</pre>
<pre class="line after"><span class="ws">        </span>return decorated_function</pre>
<pre class="line after"><span class="ws">    </span>return decorator</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span># 为常用角色提供便捷装饰器</pre>
<pre class="line after"><span class="ws"></span>def admin_required(f):</pre></div>
</div>

<li><div class="frame" id="frame-139743861877872">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/api/admin.py"</cite>,
      line <em class="line">76</em>,
      in <code class="function">manage_user</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>except ValueError:</pre>
<pre class="line before"><span class="ws">            </span>return jsonify({</pre>
<pre class="line before"><span class="ws">                </span>&#39;error&#39;: &#39;Invalid duration&#39;</pre>
<pre class="line before"><span class="ws">            </span>}), 400</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">    </span>result = AdminService.manage_user(</pre>
<pre class="line after"><span class="ws">        </span>admin_id=admin_id,</pre>
<pre class="line after"><span class="ws">        </span>user_id=user_id,</pre>
<pre class="line after"><span class="ws">        </span>action=action,</pre>
<pre class="line after"><span class="ws">        </span>reason=reason,</pre>
<pre class="line after"><span class="ws">        </span>duration=duration</pre></div>
</div>

<li><div class="frame" id="frame-139743861878544">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/services/admin_service.py"</cite>,
      line <em class="line">66</em>,
      in <code class="function">manage_user</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>&#39;success&#39;: True,</pre>
<pre class="line before"><span class="ws">                </span>&#39;message&#39;: f&#34;User {user_id} has been banned&#34;,</pre>
<pre class="line before"><span class="ws">                </span>&#39;action_id&#39;: user_action.id</pre>
<pre class="line before"><span class="ws">            </span>}</pre>
<pre class="line before"><span class="ws">        </span>elif action == &#39;unban&#39;:</pre>
<pre class="line current"><span class="ws">            </span>user_action = AdminDAO.unban_user(admin_id, user_id, reason)</pre>
<pre class="line after"><span class="ws">            </span>return {</pre>
<pre class="line after"><span class="ws">                </span>&#39;success&#39;: True,</pre>
<pre class="line after"><span class="ws">                </span>&#39;message&#39;: f&#34;User {user_id} has been unbanned&#34;,</pre>
<pre class="line after"><span class="ws">                </span>&#39;action_id&#39;: user_action.id</pre>
<pre class="line after"><span class="ws">            </span>}</pre></div>
</div>

<li><div class="frame" id="frame-139743861878880">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/dao/admin_dao.py"</cite>,
      line <em class="line">117</em>,
      in <code class="function">unban_user</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>user = User.query.get(user_id)</pre>
<pre class="line before"><span class="ws">        </span>if not user:</pre>
<pre class="line before"><span class="ws">            </span>raise ValueError(f&#34;User {user_id} not found&#34;)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if user.status != 1:  # Not banned</pre>
<pre class="line current"><span class="ws">            </span>raise ValueError(f&#34;User {user_id} is not banned&#34;)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span># Update user status</pre>
<pre class="line after"><span class="ws">        </span>user.status = 0  # Active</pre>
<pre class="line after"><span class="ws">        </span>user.banned_until = None</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>
</ul>
  <blockquote>ValueError: User 42 is not banned
</blockquote>
</div>

<div class="plain">
    <p>
      This is the Copy/Paste friendly version of the traceback.
    </p>
    <textarea cols="50" rows="10" name="code" readonly>Traceback (most recent call last):
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2213, in __call__
    return self.wsgi_app(environ, start_response)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2193, in wsgi_app
    response = self.handle_exception(e)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py&#34;, line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py&#34;, line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py&#34;, line 174, in decorator
    return current_app.ensure_sync(fn)(*args, **kwargs)
  File &#34;/home/chris/novels/backend/app/utils/auth.py&#34;, line 23, in decorated_function
    return f(*args, **kwargs)
  File &#34;/home/chris/novels/backend/app/utils/auth.py&#34;, line 43, in decorated_function
    return f(*args, **kwargs)
  File &#34;/home/chris/novels/backend/app/api/admin.py&#34;, line 76, in manage_user
    result = AdminService.manage_user(
  File &#34;/home/chris/novels/backend/app/services/admin_service.py&#34;, line 66, in manage_user
    user_action = AdminDAO.unban_user(admin_id, user_id, reason)
  File &#34;/home/chris/novels/backend/app/dao/admin_dao.py&#34;, line 117, in unban_user
    raise ValueError(f&#34;User {user_id} is not banned&#34;)
ValueError: User 42 is not banned
</textarea>
</div>
<div class="explanation">
  The debugger caught an exception in your WSGI application.  You can now
  look at the traceback which led to the error.  <span class="nojavascript">
  If you enable JavaScript you can also use additional features such as code
  execution (if the evalex feature is enabled), automatic pasting of the
  exceptions and much more.</span>
</div>
      <div class="footer">
        Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
        friendly Werkzeug powered traceback interpreter.
      </div>
    </div>

    <div class="pin-prompt">
      <div class="inner">
        <h3>Console Locked</h3>
        <p>
          The console is locked and needs to be unlocked by entering the PIN.
          You can find the PIN printed out on the standard output of your
          shell that runs the server.
        <form>
          <p>PIN:
            <input type=text name=pin size=14>
            <input type=submit name=btn value="Confirm Pin">
        </form>
      </div>
    </div>
  </body>
</html>

<!--

Traceback (most recent call last):
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py", line 174, in decorator
    return current_app.ensure_sync(fn)(*args, **kwargs)
  File "/home/chris/novels/backend/app/utils/auth.py", line 23, in decorated_function
    return f(*args, **kwargs)
  File "/home/chris/novels/backend/app/utils/auth.py", line 43, in decorated_function
    return f(*args, **kwargs)
  File "/home/chris/novels/backend/app/api/admin.py", line 76, in manage_user
    result = AdminService.manage_user(
  File "/home/chris/novels/backend/app/services/admin_service.py", line 66, in manage_user
    user_action = AdminDAO.unban_user(admin_id, user_id, reason)
  File "/home/chris/novels/backend/app/dao/admin_dao.py", line 117, in unban_user
    raise ValueError(f"User {user_id} is not banned")
ValueError: User 42 is not banned


-->

❌ 失败: 解禁请求失败，状态码: 500

================================================================================
测试: 获取用户操作历史
================================================================================
获取用户 42 的操作历史
状态码: 200
响应内容: {
  "actions": [
    {
      "action_type": "update_role",
      "admin_id": 2,
      "admin_name": "newadmin",
      "created_at": "2025-04-24T02:23:33",
      "duration": null,
      "id": 4,
      "reason": "Role updated to author",
      "target_user_id": 42,
      "target_user_name": "testuser_9352"
    }
  ],
  "page": 1,
  "per_page": 20,
  "total": 1,
  "total_pages": 1
}
❌ 失败: 成功获取用户操作历史，但未找到禁用操作记录

================================================================================
测试: 获取敏感词列表
================================================================================
获取敏感词列表...
状态码: 200
响应内容: {
  "page": 1,
  "per_page": 50,
  "total": 0,
  "total_pages": 0,
  "words": []
}
✅ 成功: 成功获取敏感词列表，共 0 条

================================================================================
测试: 添加敏感词
================================================================================
添加敏感词: test_sensitive_4578
状态码: 200
响应内容: {
  "message": "Word 'test_sensitive_4578' added to sensitive words list",
  "success": true,
  "word": {
    "added_by": 6,
    "category": "profanity",
    "created_at": "2025-04-24T02:23:34",
    "id": 4,
    "level": 2,
    "word": "test_sensitive_4578"
  }
}
✅ 成功: 成功添加敏感词，ID: 4

================================================================================
测试: 删除敏感词
================================================================================
删除敏感词 ID: 4
状态码: 200
响应内容: {
  "message": "Word deleted",
  "success": true
}
✅ 成功: 成功删除敏感词

================================================================================
测试: 获取待审核内容
================================================================================
获取待审核的 novel 内容...
状态码: 200
响应内容: {
  "content": [],
  "content_type": "novel",
  "page": 1,
  "per_page": 20,
  "total": 0,
  "total_pages": 0
}
✅ 成功: 成功获取待审核的 novel 内容列表
获取待审核的 chapter 内容...
状态码: 200
响应内容: {
  "content": [],
  "content_type": "chapter",
  "page": 1,
  "per_page": 20,
  "total": 0,
  "total_pages": 0
}
✅ 成功: 成功获取待审核的 chapter 内容列表
获取待审核的 comment 内容...
状态码: 200
响应内容: {
  "content": [],
  "content_type": "comment",
  "page": 1,
  "per_page": 20,
  "total": 0,
  "total_pages": 0
}
✅ 成功: 成功获取待审核的 comment 内容列表

================================================================================
测试: 注销作者身份
================================================================================
注销作者身份...
状态码: 200
响应内容: {
  "message": "您已成功放弃作者身份",
  "success": true
}
✅ 成功: 成功注销作者身份

================================================================================
测试: 注销作者用户账户
================================================================================
注销作者用户账户...
状态码: 200
响应内容: {
  "message": "Account successfully deactivated",
  "success": true
}
✅ 成功: 成功注销作者用户账户

================================================================================
测试: 注销普通用户账户
================================================================================
注销普通用户账户...
状态码: 500
响应内容: <!doctype html>
<html lang=en>
  <head>
    <title>sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1048, &#34;Column &#39;target_user_id&#39; cannot be null&#34;)
[SQL: UPDATE user_action SET target_user_id=%(target_user_id)s WHERE user_action.id = %(user_action_id)s]
[parameters: {&#39;target_user_id&#39;: None, &#39;user_action_id&#39;: 4}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
 // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css">
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script>
      var CONSOLE_MODE = false,
          EVALEX = true,
          EVALEX_TRUSTED = false,
          SECRET = "hGZxCLme2nil2UPZIPjG";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
<h1>IntegrityError</h1>
<div class="detail">
  <p class="errormsg">sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1048, &#34;Column &#39;target_user_id&#39; cannot be null&#34;)
[SQL: UPDATE user_action SET target_user_id=%(target_user_id)s WHERE user_action.id = %(user_action_id)s]
[parameters: {&#39;target_user_id&#39;: None, &#39;user_action_id&#39;: 4}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
</p>
</div>
<h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
<div class="traceback">
  <h3></h3>
  <ul><li><div class="frame" id="frame-139743860708896">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1964</em>,
      in <code class="function">_exec_single_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                            </span>context,</pre>
<pre class="line before"><span class="ws">                        </span>):</pre>
<pre class="line before"><span class="ws">                            </span>evt_handled = True</pre>
<pre class="line before"><span class="ws">                            </span>break</pre>
<pre class="line before"><span class="ws">                </span>if not evt_handled:</pre>
<pre class="line current"><span class="ws">                    </span>self.dialect.do_execute(</pre>
<pre class="line after"><span class="ws">                        </span>cursor, str_statement, effective_parameters, context</pre>
<pre class="line after"><span class="ws">                    </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if self._has_events or self.engine._has_events:</pre>
<pre class="line after"><span class="ws">                </span>self.dispatch.after_cursor_execute(</pre></div>
</div>

<li><div class="frame" id="frame-139743860709008">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py"</cite>,
      line <em class="line">945</em>,
      in <code class="function">do_execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_executemany(self, cursor, statement, parameters, context=None):</pre>
<pre class="line before"><span class="ws">        </span>cursor.executemany(statement, parameters)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_execute(self, cursor, statement, parameters, context=None):</pre>
<pre class="line current"><span class="ws">        </span>cursor.execute(statement, parameters)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def do_execute_no_params(self, cursor, statement, context=None):</pre>
<pre class="line after"><span class="ws">        </span>cursor.execute(statement)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def is_disconnect(</pre></div>
</div>

<li><div class="frame" id="frame-139743860709120">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">153</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>while self.nextset():</pre>
<pre class="line before"><span class="ws">            </span>pass</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>query = self.mogrify(query, args)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>result = self._query(query)</pre>
<pre class="line after"><span class="ws">        </span>self._executed = query</pre>
<pre class="line after"><span class="ws">        </span>return result</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def executemany(self, query, args):</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Run several data against one query.</pre></div>
</div>

<li><div class="frame" id="frame-139743860709232">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">322</em>,
      in <code class="function">_query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rownumber = r</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def _query(self, q):</pre>
<pre class="line before"><span class="ws">        </span>conn = self._get_db()</pre>
<pre class="line before"><span class="ws">        </span>self._clear_result()</pre>
<pre class="line current"><span class="ws">        </span>conn.query(q)</pre>
<pre class="line after"><span class="ws">        </span>self._do_get_result()</pre>
<pre class="line after"><span class="ws">        </span>return self.rowcount</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _clear_result(self):</pre>
<pre class="line after"><span class="ws">        </span>self.rownumber = 0</pre></div>
</div>

<li><div class="frame" id="frame-139743860709344">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">558</em>,
      in <code class="function">query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># if DEBUG:</pre>
<pre class="line before"><span class="ws">        </span>#     print(&#34;DEBUG: sending query:&#34;, sql)</pre>
<pre class="line before"><span class="ws">        </span>if isinstance(sql, str):</pre>
<pre class="line before"><span class="ws">            </span>sql = sql.encode(self.encoding, &#34;surrogateescape&#34;)</pre>
<pre class="line before"><span class="ws">        </span>self._execute_command(COMMAND.COM_QUERY, sql)</pre>
<pre class="line current"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def next_result(self, unbuffered=False):</pre>
<pre class="line after"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre></div>
</div>

<li><div class="frame" id="frame-139743860709456">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">822</em>,
      in <code class="function">_read_query_result</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>result.unbuffered_active = False</pre>
<pre class="line before"><span class="ws">                </span>result.connection = None</pre>
<pre class="line before"><span class="ws">                </span>raise</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line before"><span class="ws">            </span>result = MySQLResult(self)</pre>
<pre class="line current"><span class="ws">            </span>result.read()</pre>
<pre class="line after"><span class="ws">        </span>self._result = result</pre>
<pre class="line after"><span class="ws">        </span>if result.server_status is not None:</pre>
<pre class="line after"><span class="ws">            </span>self.server_status = result.server_status</pre>
<pre class="line after"><span class="ws">        </span>return result.affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860709568">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">1200</em>,
      in <code class="function">read</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>if self.unbuffered_active:</pre>
<pre class="line before"><span class="ws">            </span>self._finish_unbuffered_query()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def read(self):</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line current"><span class="ws">            </span>first_packet = self.connection._read_packet()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if first_packet.is_ok_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_ok_packet(first_packet)</pre>
<pre class="line after"><span class="ws">            </span>elif first_packet.is_load_local_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_load_local_packet(first_packet)</pre></div>
</div>

<li><div class="frame" id="frame-139743860709680">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">772</em>,
      in <code class="function">_read_packet</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>packet = packet_type(bytes(buff), self.encoding)</pre>
<pre class="line before"><span class="ws">        </span>if packet.is_error_packet():</pre>
<pre class="line before"><span class="ws">            </span>if self._result is not None and self._result.unbuffered_active is True:</pre>
<pre class="line before"><span class="ws">                </span>self._result.unbuffered_active = False</pre>
<pre class="line current"><span class="ws">            </span>packet.raise_for_error()</pre>
<pre class="line after"><span class="ws">        </span>return packet</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _read_bytes(self, num_bytes):</pre>
<pre class="line after"><span class="ws">        </span>self._sock.settimeout(self._read_timeout)</pre>
<pre class="line after"><span class="ws">        </span>while True:</pre></div>
</div>

<li><div class="frame" id="frame-139743860709792">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py"</cite>,
      line <em class="line">221</em>,
      in <code class="function">raise_for_error</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rewind()</pre>
<pre class="line before"><span class="ws">        </span>self.advance(1)  # field_count == error (we already know that)</pre>
<pre class="line before"><span class="ws">        </span>errno = self.read_uint16()</pre>
<pre class="line before"><span class="ws">        </span>if DEBUG:</pre>
<pre class="line before"><span class="ws">            </span>print(&#34;errno =&#34;, errno)</pre>
<pre class="line current"><span class="ws">        </span>err.raise_mysql_exception(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def dump(self):</pre>
<pre class="line after"><span class="ws">        </span>dump_packet(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860709904">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py"</cite>,
      line <em class="line">143</em>,
      in <code class="function">raise_mysql_exception</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>errno = struct.unpack(&#34;&lt;h&#34;, data[1:3])[0]</pre>
<pre class="line before"><span class="ws">    </span>errval = data[9:].decode(&#34;utf-8&#34;, &#34;replace&#34;)</pre>
<pre class="line before"><span class="ws">    </span>errorclass = error_map.get(errno)</pre>
<pre class="line before"><span class="ws">    </span>if errorclass is None:</pre>
<pre class="line before"><span class="ws">        </span>errorclass = InternalError if errno &lt; 1000 else OperationalError</pre>
<pre class="line current"><span class="ws">    </span>raise errorclass(errno, errval)</pre></div>
</div>

<li><div class="exc-divider">The above exception was the direct cause of the following exception:</div>
<li><div class="frame" id="frame-139743861882240">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2213</em>,
      in <code class="function">__call__</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>def __call__(self, environ: dict, start_response: t.Callable) -&gt; t.Any:</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;The WSGI server calls the Flask application object as the</pre>
<pre class="line before"><span class="ws">        </span>WSGI application. This calls :meth:`wsgi_app`, which can be</pre>
<pre class="line before"><span class="ws">        </span>wrapped to apply middleware.</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line current"><span class="ws">        </span>return self.wsgi_app(environ, start_response)</pre></div>
</div>

<li><div class="frame" id="frame-139743861871152">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2193</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line before"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line before"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line before"><span class="ws">                </span>error = e</pre>
<pre class="line current"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>return response(environ, start_response)</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre></div>
</div>

<li><div class="frame" id="frame-139743861879440">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py"</cite>,
      line <em class="line">176</em>,
      in <code class="function">wrapped_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># Wrap exception handlers with cross_origin</pre>
<pre class="line before"><span class="ws">        </span># These error handlers will still respect the behavior of the route</pre>
<pre class="line before"><span class="ws">        </span>if options.get(&#39;intercept_exceptions&#39;, True):</pre>
<pre class="line before"><span class="ws">            </span>def _after_request_decorator(f):</pre>
<pre class="line before"><span class="ws">                </span>def wrapped_function(*args, **kwargs):</pre>
<pre class="line current"><span class="ws">                    </span>return cors_after_request(app.make_response(f(*args, **kwargs)))</pre>
<pre class="line after"><span class="ws">                </span>return wrapped_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if hasattr(app, &#39;handle_exception&#39;):</pre>
<pre class="line after"><span class="ws">                </span>app.handle_exception = _after_request_decorator(</pre>
<pre class="line after"><span class="ws">                    </span>app.handle_exception)</pre></div>
</div>

<li><div class="frame" id="frame-139743861868800">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">2190</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>ctx = self.request_context(environ)</pre>
<pre class="line before"><span class="ws">        </span>error: BaseException | None = None</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line current"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line after"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">                </span>error = e</pre>
<pre class="line after"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre></div>
</div>

<li><div class="frame" id="frame-139743861881792">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1486</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line before"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line before"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line current"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>rv: ft.ResponseReturnValue | HTTPException,</pre></div>
</div>

<li><div class="frame" id="frame-139743861881904">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py"</cite>,
      line <em class="line">176</em>,
      in <code class="function">wrapped_function</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># Wrap exception handlers with cross_origin</pre>
<pre class="line before"><span class="ws">        </span># These error handlers will still respect the behavior of the route</pre>
<pre class="line before"><span class="ws">        </span>if options.get(&#39;intercept_exceptions&#39;, True):</pre>
<pre class="line before"><span class="ws">            </span>def _after_request_decorator(f):</pre>
<pre class="line before"><span class="ws">                </span>def wrapped_function(*args, **kwargs):</pre>
<pre class="line current"><span class="ws">                    </span>return cors_after_request(app.make_response(f(*args, **kwargs)))</pre>
<pre class="line after"><span class="ws">                </span>return wrapped_function</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if hasattr(app, &#39;handle_exception&#39;):</pre>
<pre class="line after"><span class="ws">                </span>app.handle_exception = _after_request_decorator(</pre>
<pre class="line after"><span class="ws">                    </span>app.handle_exception)</pre></div>
</div>

<li><div class="frame" id="frame-139743861878656">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1484</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line current"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line after"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre></div>
</div>

<li><div class="frame" id="frame-139743861867232">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask/app.py"</cite>,
      line <em class="line">1469</em>,
      in <code class="function">dispatch_request</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>and req.method == &#34;OPTIONS&#34;</pre>
<pre class="line before"><span class="ws">        </span>):</pre>
<pre class="line before"><span class="ws">            </span>return self.make_default_options_response()</pre>
<pre class="line before"><span class="ws">        </span># otherwise dispatch to the handler for that endpoint</pre>
<pre class="line before"><span class="ws">        </span>view_args: dict[str, t.Any] = req.view_args  # type: ignore[assignment]</pre>
<pre class="line current"><span class="ws">        </span>return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def full_dispatch_request(self) -&gt; Response:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Dispatches the request and on top of that performs request</pre>
<pre class="line after"><span class="ws">        </span>pre and postprocessing as well as HTTP exception catching and</pre>
<pre class="line after"><span class="ws">        </span>error handling.</pre></div>
</div>

<li><div class="frame" id="frame-139743861882576">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py"</cite>,
      line <em class="line">174</em>,
      in <code class="function">decorator</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>@wraps(fn)</pre>
<pre class="line before"><span class="ws">        </span>def decorator(*args, **kwargs):</pre>
<pre class="line before"><span class="ws">            </span>verify_jwt_in_request(</pre>
<pre class="line before"><span class="ws">                </span>optional, fresh, refresh, locations, verify_type, skip_revocation_check</pre>
<pre class="line before"><span class="ws">            </span>)</pre>
<pre class="line current"><span class="ws">            </span>return current_app.ensure_sync(fn)(*args, **kwargs)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>return decorator</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>return wrapper</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743861881568">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/api/user.py"</cite>,
      line <em class="line">181</em>,
      in <code class="function">deactivate_account</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>password = data.get(&#39;password&#39;)</pre>
<pre class="line before"><span class="ws">    </span>if not password:</pre>
<pre class="line before"><span class="ws">        </span>return jsonify({&#39;error&#39;: &#39;Password is required for account deactivation&#39;}), 400</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span># Call service to handle account deactivation</pre>
<pre class="line current"><span class="ws">    </span>result = UserService.deactivate_account(user_id, password)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>if not result[&#39;success&#39;]:</pre>
<pre class="line after"><span class="ws">        </span>return jsonify({&#39;error&#39;: result[&#39;error&#39;]}), 400</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>return jsonify({</pre></div>
</div>

<li><div class="frame" id="frame-139743861881680">
  <h4>File <cite class="filename">"/home/chris/novels/backend/app/services/user_service.py"</cite>,
      line <em class="line">476</em>,
      in <code class="function">deactivate_account</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>UserFollowing.query.filter_by(follower_id=user_id).delete()</pre>
<pre class="line before"><span class="ws">        </span>UserFollowing.query.filter_by(followed_id=user_id).delete()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span># Delete the user</pre>
<pre class="line before"><span class="ws">        </span>db.session.delete(user)</pre>
<pre class="line current"><span class="ws">        </span>db.session.commit()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>return {</pre>
<pre class="line after"><span class="ws">            </span>&#39;success&#39;: True,</pre>
<pre class="line after"><span class="ws">            </span>&#39;message&#39;: &#39;Account successfully deactivated&#39;</pre>
<pre class="line after"><span class="ws">        </span>}</pre></div>
</div>

<li><div class="frame" id="frame-139743860705312">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/scoping.py"</cite>,
      line <em class="line">599</em>,
      in <code class="function">commit</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>:ref:`asyncio_orm_avoid_lazyloads`</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;  # noqa: E501</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>return self._proxied.commit()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def connection(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>bind_arguments: Optional[_BindArguments] = None,</pre>
<pre class="line after"><span class="ws">        </span>execution_options: Optional[CoreExecuteOptionsParameter] = None,</pre></div>
</div>

<li><div class="frame" id="frame-139743860705424">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">2032</em>,
      in <code class="function">commit</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>trans = self._transaction</pre>
<pre class="line before"><span class="ws">        </span>if trans is None:</pre>
<pre class="line before"><span class="ws">            </span>trans = self._autobegin_t()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>trans.commit(_to_root=True)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def prepare(self) -&gt; None:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Prepare the current transaction in progress for two phase commit.</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>If no transaction is in progress, this method raises an</pre></div>
</div>

<li><div class="frame" id="frame-139743860705536">
  <h4>File <cite class="filename">"&lt;string&gt;"</cite>,
      line <em class="line">2</em>,
      in <code class="function">commit</code></h4>
  <div class="source "></div>
</div>

<li><div class="frame" id="frame-139743860705648">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py"</cite>,
      line <em class="line">139</em>,
      in <code class="function">_go</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                    </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>self._current_fn = fn</pre>
<pre class="line before"><span class="ws">            </span>self._next_state = _StateChangeStates.CHANGE_IN_PROGRESS</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>ret_value = fn(self, *arg, **kw)</pre>
<pre class="line after"><span class="ws">            </span>except:</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>if self._state is expect_state:</pre>
<pre class="line after"><span class="ws">                    </span>return ret_value</pre></div>
</div>

<li><div class="frame" id="frame-139743860705760">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">1313</em>,
      in <code class="function">commit</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>SessionTransactionState.CLOSED,</pre>
<pre class="line before"><span class="ws">    </span>)</pre>
<pre class="line before"><span class="ws">    </span>def commit(self, _to_root: bool = False) -&gt; None:</pre>
<pre class="line before"><span class="ws">        </span>if self._state is not SessionTransactionState.PREPARED:</pre>
<pre class="line before"><span class="ws">            </span>with self._expect_state(SessionTransactionState.PREPARED):</pre>
<pre class="line current"><span class="ws">                </span>self._prepare_impl()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>if self._parent is None or self.nested:</pre>
<pre class="line after"><span class="ws">            </span>for conn, trans, should_commit, autoclose in set(</pre>
<pre class="line after"><span class="ws">                </span>self._connections.values()</pre>
<pre class="line after"><span class="ws">            </span>):</pre></div>
</div>

<li><div class="frame" id="frame-139743860705872">
  <h4>File <cite class="filename">"&lt;string&gt;"</cite>,
      line <em class="line">2</em>,
      in <code class="function">_prepare_impl</code></h4>
  <div class="source "></div>
</div>

<li><div class="frame" id="frame-139743860705984">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py"</cite>,
      line <em class="line">139</em>,
      in <code class="function">_go</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                    </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>self._current_fn = fn</pre>
<pre class="line before"><span class="ws">            </span>self._next_state = _StateChangeStates.CHANGE_IN_PROGRESS</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>ret_value = fn(self, *arg, **kw)</pre>
<pre class="line after"><span class="ws">            </span>except:</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>if self._state is expect_state:</pre>
<pre class="line after"><span class="ws">                    </span>return ret_value</pre></div>
</div>

<li><div class="frame" id="frame-139743860706096">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">1288</em>,
      in <code class="function">_prepare_impl</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if not self.session._flushing:</pre>
<pre class="line before"><span class="ws">            </span>for _flush_guard in range(100):</pre>
<pre class="line before"><span class="ws">                </span>if self.session._is_clean():</pre>
<pre class="line before"><span class="ws">                    </span>break</pre>
<pre class="line current"><span class="ws">                </span>self.session.flush()</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>raise exc.FlushError(</pre>
<pre class="line after"><span class="ws">                    </span>&#34;Over 100 subsequent flushes have occurred within &#34;</pre>
<pre class="line after"><span class="ws">                    </span>&#34;session.commit() - is an after_flush() hook &#34;</pre>
<pre class="line after"><span class="ws">                    </span>&#34;creating new objects?&#34;</pre></div>
</div>

<li><div class="frame" id="frame-139743860706208">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">4353</em>,
      in <code class="function">flush</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if self._is_clean():</pre>
<pre class="line before"><span class="ws">            </span>return</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>self._flushing = True</pre>
<pre class="line current"><span class="ws">            </span>self._flush(objects)</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre>
<pre class="line after"><span class="ws">            </span>self._flushing = False</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _flush_warning(self, method: Any) -&gt; None:</pre>
<pre class="line after"><span class="ws">        </span>util.warn(</pre></div>
</div>

<li><div class="frame" id="frame-139743860706320">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">4488</em>,
      in <code class="function">_flush</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>self.dispatch.after_flush_postexec(self, flush_context)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>transaction.commit()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>except:</pre>
<pre class="line current"><span class="ws">            </span>with util.safe_reraise():</pre>
<pre class="line after"><span class="ws">                </span>transaction.rollback(_capture_exception=True)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def bulk_save_objects(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>objects: Iterable[object],</pre></div>
</div>

<li><div class="frame" id="frame-139743860706432">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py"</cite>,
      line <em class="line">146</em>,
      in <code class="function">__exit__</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># see #2703 for notes</pre>
<pre class="line before"><span class="ws">        </span>if type_ is None:</pre>
<pre class="line before"><span class="ws">            </span>exc_type, exc_value, exc_tb = self._exc_info</pre>
<pre class="line before"><span class="ws">            </span>assert exc_value is not None</pre>
<pre class="line before"><span class="ws">            </span>self._exc_info = None  # remove potential circular references</pre>
<pre class="line current"><span class="ws">            </span>raise exc_value.with_traceback(exc_tb)</pre>
<pre class="line after"><span class="ws">        </span>else:</pre>
<pre class="line after"><span class="ws">            </span>self._exc_info = None  # remove potential circular references</pre>
<pre class="line after"><span class="ws">            </span>assert value is not None</pre>
<pre class="line after"><span class="ws">            </span>raise value.with_traceback(traceback)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860706544">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py"</cite>,
      line <em class="line">4449</em>,
      in <code class="function">_flush</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>flush_context.transaction = transaction = self._autobegin_t()._begin()</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>self._warn_on_events = True</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>flush_context.execute()</pre>
<pre class="line after"><span class="ws">            </span>finally:</pre>
<pre class="line after"><span class="ws">                </span>self._warn_on_events = False</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>self.dispatch.after_flush(self, flush_context)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860706656">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py"</cite>,
      line <em class="line">466</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>while set_:</pre>
<pre class="line before"><span class="ws">                    </span>n = set_.pop()</pre>
<pre class="line before"><span class="ws">                    </span>n.execute_aggregate(self, set_)</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line before"><span class="ws">            </span>for rec in topological.sort(self.dependencies, postsort_actions):</pre>
<pre class="line current"><span class="ws">                </span>rec.execute(self)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_flush_changes(self) -&gt; None:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Mark processed objects as clean / deleted after a successful</pre>
<pre class="line after"><span class="ws">        </span>flush().</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860706768">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py"</cite>,
      line <em class="line">642</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.sort_key = (&#34;SaveUpdateAll&#34;, mapper._sort_key)</pre>
<pre class="line before"><span class="ws">        </span>assert mapper is mapper.base_mapper</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>@util.preload_module(&#34;sqlalchemy.orm.persistence&#34;)</pre>
<pre class="line before"><span class="ws">    </span>def execute(self, uow):</pre>
<pre class="line current"><span class="ws">        </span>util.preloaded.orm_persistence.save_obj(</pre>
<pre class="line after"><span class="ws">            </span>self.mapper,</pre>
<pre class="line after"><span class="ws">            </span>uow.states_for_mapper_hierarchy(self.mapper, False, False),</pre>
<pre class="line after"><span class="ws">            </span>uow,</pre>
<pre class="line after"><span class="ws">        </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860706880">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py"</cite>,
      line <em class="line">85</em>,
      in <code class="function">save_obj</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>update = _collect_update_commands(</pre>
<pre class="line before"><span class="ws">            </span>uowtransaction, table, states_to_update</pre>
<pre class="line before"><span class="ws">        </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>_emit_update_statements(</pre>
<pre class="line after"><span class="ws">            </span>base_mapper,</pre>
<pre class="line after"><span class="ws">            </span>uowtransaction,</pre>
<pre class="line after"><span class="ws">            </span>mapper,</pre>
<pre class="line after"><span class="ws">            </span>table,</pre>
<pre class="line after"><span class="ws">            </span>update,</pre></div>
</div>

<li><div class="frame" id="frame-139743860706992">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py"</cite>,
      line <em class="line">912</em>,
      in <code class="function">_emit_update_statements</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>check_rowcount = enable_check_rowcount and (</pre>
<pre class="line before"><span class="ws">                    </span>assert_multirow</pre>
<pre class="line before"><span class="ws">                    </span>or (assert_singlerow and len(multiparams) == 1)</pre>
<pre class="line before"><span class="ws">                </span>)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">                </span>c = connection.execute(</pre>
<pre class="line after"><span class="ws">                    </span>statement, multiparams, execution_options=execution_options</pre>
<pre class="line after"><span class="ws">                </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">                </span>rows += c.rowcount</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860707104">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1416</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>meth = statement._execute_on_connection</pre>
<pre class="line before"><span class="ws">        </span>except AttributeError as err:</pre>
<pre class="line before"><span class="ws">            </span>raise exc.ObjectNotExecutableError(statement) from err</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line current"><span class="ws">            </span>return meth(</pre>
<pre class="line after"><span class="ws">                </span>self,</pre>
<pre class="line after"><span class="ws">                </span>distilled_parameters,</pre>
<pre class="line after"><span class="ws">                </span>execution_options or NO_OPTIONS,</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860707216">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/sql/elements.py"</cite>,
      line <em class="line">523</em>,
      in <code class="function">_execute_on_connection</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>execution_options: CoreExecuteOptionsParameter,</pre>
<pre class="line before"><span class="ws">    </span>) -&gt; Result[Any]:</pre>
<pre class="line before"><span class="ws">        </span>if self.supports_execution:</pre>
<pre class="line before"><span class="ws">            </span>if TYPE_CHECKING:</pre>
<pre class="line before"><span class="ws">                </span>assert isinstance(self, Executable)</pre>
<pre class="line current"><span class="ws">            </span>return connection._execute_clauseelement(</pre>
<pre class="line after"><span class="ws">                </span>self, distilled_params, execution_options</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws">        </span>else:</pre>
<pre class="line after"><span class="ws">            </span>raise exc.ObjectNotExecutableError(self)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860707328">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1638</em>,
      in <code class="function">_execute_clauseelement</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>column_keys=keys,</pre>
<pre class="line before"><span class="ws">            </span>for_executemany=for_executemany,</pre>
<pre class="line before"><span class="ws">            </span>schema_translate_map=schema_translate_map,</pre>
<pre class="line before"><span class="ws">            </span>linting=self.dialect.compiler_linting | compiler.WARN_LINTING,</pre>
<pre class="line before"><span class="ws">        </span>)</pre>
<pre class="line current"><span class="ws">        </span>ret = self._execute_context(</pre>
<pre class="line after"><span class="ws">            </span>dialect,</pre>
<pre class="line after"><span class="ws">            </span>dialect.execution_ctx_cls._init_compiled,</pre>
<pre class="line after"><span class="ws">            </span>compiled_sql,</pre>
<pre class="line after"><span class="ws">            </span>distilled_parameters,</pre>
<pre class="line after"><span class="ws">            </span>execution_options,</pre></div>
</div>

<li><div class="frame" id="frame-139743860707440">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1843</em>,
      in <code class="function">_execute_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>context.pre_exec()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>if context.execute_style is ExecuteStyle.INSERTMANYVALUES:</pre>
<pre class="line before"><span class="ws">            </span>return self._exec_insertmany_context(dialect, context)</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line current"><span class="ws">            </span>return self._exec_single_context(</pre>
<pre class="line after"><span class="ws">                </span>dialect, context, statement, parameters</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _exec_single_context(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre></div>
</div>

<li><div class="frame" id="frame-139743860707552">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1983</em>,
      in <code class="function">_exec_single_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>context.post_exec()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>result = context._setup_result_proxy()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>except BaseException as e:</pre>
<pre class="line current"><span class="ws">            </span>self._handle_dbapi_exception(</pre>
<pre class="line after"><span class="ws">                </span>e, str_statement, effective_parameters, cursor, context</pre>
<pre class="line after"><span class="ws">            </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>return result</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860707664">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">2352</em>,
      in <code class="function">_handle_dbapi_exception</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>if newraise:</pre>
<pre class="line before"><span class="ws">                </span>raise newraise.with_traceback(exc_info[2]) from e</pre>
<pre class="line before"><span class="ws">            </span>elif should_wrap:</pre>
<pre class="line before"><span class="ws">                </span>assert sqlalchemy_exception is not None</pre>
<pre class="line current"><span class="ws">                </span>raise sqlalchemy_exception.with_traceback(exc_info[2]) from e</pre>
<pre class="line after"><span class="ws">            </span>else:</pre>
<pre class="line after"><span class="ws">                </span>assert exc_info[1] is not None</pre>
<pre class="line after"><span class="ws">                </span>raise exc_info[1].with_traceback(exc_info[2])</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre>
<pre class="line after"><span class="ws">            </span>del self._reentrant_error</pre></div>
</div>

<li><div class="frame" id="frame-139743860707776">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py"</cite>,
      line <em class="line">1964</em>,
      in <code class="function">_exec_single_context</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                            </span>context,</pre>
<pre class="line before"><span class="ws">                        </span>):</pre>
<pre class="line before"><span class="ws">                            </span>evt_handled = True</pre>
<pre class="line before"><span class="ws">                            </span>break</pre>
<pre class="line before"><span class="ws">                </span>if not evt_handled:</pre>
<pre class="line current"><span class="ws">                    </span>self.dialect.do_execute(</pre>
<pre class="line after"><span class="ws">                        </span>cursor, str_statement, effective_parameters, context</pre>
<pre class="line after"><span class="ws">                    </span>)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if self._has_events or self.engine._has_events:</pre>
<pre class="line after"><span class="ws">                </span>self.dispatch.after_cursor_execute(</pre></div>
</div>

<li><div class="frame" id="frame-139743860707888">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py"</cite>,
      line <em class="line">945</em>,
      in <code class="function">do_execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_executemany(self, cursor, statement, parameters, context=None):</pre>
<pre class="line before"><span class="ws">        </span>cursor.executemany(statement, parameters)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def do_execute(self, cursor, statement, parameters, context=None):</pre>
<pre class="line current"><span class="ws">        </span>cursor.execute(statement, parameters)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def do_execute_no_params(self, cursor, statement, context=None):</pre>
<pre class="line after"><span class="ws">        </span>cursor.execute(statement)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def is_disconnect(</pre></div>
</div>

<li><div class="frame" id="frame-139743860708000">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">153</em>,
      in <code class="function">execute</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>while self.nextset():</pre>
<pre class="line before"><span class="ws">            </span>pass</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>query = self.mogrify(query, args)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>result = self._query(query)</pre>
<pre class="line after"><span class="ws">        </span>self._executed = query</pre>
<pre class="line after"><span class="ws">        </span>return result</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def executemany(self, query, args):</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Run several data against one query.</pre></div>
</div>

<li><div class="frame" id="frame-139743860708112">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py"</cite>,
      line <em class="line">322</em>,
      in <code class="function">_query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rownumber = r</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def _query(self, q):</pre>
<pre class="line before"><span class="ws">        </span>conn = self._get_db()</pre>
<pre class="line before"><span class="ws">        </span>self._clear_result()</pre>
<pre class="line current"><span class="ws">        </span>conn.query(q)</pre>
<pre class="line after"><span class="ws">        </span>self._do_get_result()</pre>
<pre class="line after"><span class="ws">        </span>return self.rowcount</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _clear_result(self):</pre>
<pre class="line after"><span class="ws">        </span>self.rownumber = 0</pre></div>
</div>

<li><div class="frame" id="frame-139743860708224">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">558</em>,
      in <code class="function">query</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span># if DEBUG:</pre>
<pre class="line before"><span class="ws">        </span>#     print(&#34;DEBUG: sending query:&#34;, sql)</pre>
<pre class="line before"><span class="ws">        </span>if isinstance(sql, str):</pre>
<pre class="line before"><span class="ws">            </span>sql = sql.encode(self.encoding, &#34;surrogateescape&#34;)</pre>
<pre class="line before"><span class="ws">        </span>self._execute_command(COMMAND.COM_QUERY, sql)</pre>
<pre class="line current"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def next_result(self, unbuffered=False):</pre>
<pre class="line after"><span class="ws">        </span>self._affected_rows = self._read_query_result(unbuffered=unbuffered)</pre>
<pre class="line after"><span class="ws">        </span>return self._affected_rows</pre></div>
</div>

<li><div class="frame" id="frame-139743860708336">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">822</em>,
      in <code class="function">_read_query_result</code></h4>
  <div class="source "><pre class="line before"><span class="ws">                </span>result.unbuffered_active = False</pre>
<pre class="line before"><span class="ws">                </span>result.connection = None</pre>
<pre class="line before"><span class="ws">                </span>raise</pre>
<pre class="line before"><span class="ws">        </span>else:</pre>
<pre class="line before"><span class="ws">            </span>result = MySQLResult(self)</pre>
<pre class="line current"><span class="ws">            </span>result.read()</pre>
<pre class="line after"><span class="ws">        </span>self._result = result</pre>
<pre class="line after"><span class="ws">        </span>if result.server_status is not None:</pre>
<pre class="line after"><span class="ws">            </span>self.server_status = result.server_status</pre>
<pre class="line after"><span class="ws">        </span>return result.affected_rows</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860708448">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">1200</em>,
      in <code class="function">read</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>if self.unbuffered_active:</pre>
<pre class="line before"><span class="ws">            </span>self._finish_unbuffered_query()</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span>def read(self):</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line current"><span class="ws">            </span>first_packet = self.connection._read_packet()</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>if first_packet.is_ok_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_ok_packet(first_packet)</pre>
<pre class="line after"><span class="ws">            </span>elif first_packet.is_load_local_packet():</pre>
<pre class="line after"><span class="ws">                </span>self._read_load_local_packet(first_packet)</pre></div>
</div>

<li><div class="frame" id="frame-139743860708560">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py"</cite>,
      line <em class="line">772</em>,
      in <code class="function">_read_packet</code></h4>
  <div class="source "><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>packet = packet_type(bytes(buff), self.encoding)</pre>
<pre class="line before"><span class="ws">        </span>if packet.is_error_packet():</pre>
<pre class="line before"><span class="ws">            </span>if self._result is not None and self._result.unbuffered_active is True:</pre>
<pre class="line before"><span class="ws">                </span>self._result.unbuffered_active = False</pre>
<pre class="line current"><span class="ws">            </span>packet.raise_for_error()</pre>
<pre class="line after"><span class="ws">        </span>return packet</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _read_bytes(self, num_bytes):</pre>
<pre class="line after"><span class="ws">        </span>self._sock.settimeout(self._read_timeout)</pre>
<pre class="line after"><span class="ws">        </span>while True:</pre></div>
</div>

<li><div class="frame" id="frame-139743860708672">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py"</cite>,
      line <em class="line">221</em>,
      in <code class="function">raise_for_error</code></h4>
  <div class="source "><pre class="line before"><span class="ws">        </span>self.rewind()</pre>
<pre class="line before"><span class="ws">        </span>self.advance(1)  # field_count == error (we already know that)</pre>
<pre class="line before"><span class="ws">        </span>errno = self.read_uint16()</pre>
<pre class="line before"><span class="ws">        </span>if DEBUG:</pre>
<pre class="line before"><span class="ws">            </span>print(&#34;errno =&#34;, errno)</pre>
<pre class="line current"><span class="ws">        </span>err.raise_mysql_exception(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def dump(self):</pre>
<pre class="line after"><span class="ws">        </span>dump_packet(self._data)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-139743860708784">
  <h4>File <cite class="filename">"/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py"</cite>,
      line <em class="line">143</em>,
      in <code class="function">raise_mysql_exception</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>errno = struct.unpack(&#34;&lt;h&#34;, data[1:3])[0]</pre>
<pre class="line before"><span class="ws">    </span>errval = data[9:].decode(&#34;utf-8&#34;, &#34;replace&#34;)</pre>
<pre class="line before"><span class="ws">    </span>errorclass = error_map.get(errno)</pre>
<pre class="line before"><span class="ws">    </span>if errorclass is None:</pre>
<pre class="line before"><span class="ws">        </span>errorclass = InternalError if errno &lt; 1000 else OperationalError</pre>
<pre class="line current"><span class="ws">    </span>raise errorclass(errno, errval)</pre></div>
</div>
</ul>
  <blockquote>sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1048, &#34;Column &#39;target_user_id&#39; cannot be null&#34;)
[SQL: UPDATE user_action SET target_user_id=%(target_user_id)s WHERE user_action.id = %(user_action_id)s]
[parameters: {&#39;target_user_id&#39;: None, &#39;user_action_id&#39;: 4}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
</blockquote>
</div>

<div class="plain">
    <p>
      This is the Copy/Paste friendly version of the traceback.
    </p>
    <textarea cols="50" rows="10" name="code" readonly>Traceback (most recent call last):
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1964, in _exec_single_context
    self.dialect.do_execute(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py&#34;, line 945, in do_execute
    cursor.execute(statement, parameters)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 153, in execute
    result = self._query(query)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 322, in _query
    conn.query(q)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 822, in _read_query_result
    result.read()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 1200, in read
    first_packet = self.connection._read_packet()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 772, in _read_packet
    packet.raise_for_error()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py&#34;, line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py&#34;, line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.IntegrityError: (1048, &#34;Column &#39;target_user_id&#39; cannot be null&#34;)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2213, in __call__
    return self.wsgi_app(environ, start_response)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2193, in wsgi_app
    response = self.handle_exception(e)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py&#34;, line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py&#34;, line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask/app.py&#34;, line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py&#34;, line 174, in decorator
    return current_app.ensure_sync(fn)(*args, **kwargs)
  File &#34;/home/chris/novels/backend/app/api/user.py&#34;, line 181, in deactivate_account
    result = UserService.deactivate_account(user_id, password)
  File &#34;/home/chris/novels/backend/app/services/user_service.py&#34;, line 476, in deactivate_account
    db.session.commit()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/scoping.py&#34;, line 599, in commit
    return self._proxied.commit()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 2032, in commit
    trans.commit(_to_root=True)
  File &#34;&lt;string&gt;&#34;, line 2, in commit
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py&#34;, line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 1313, in commit
    self._prepare_impl()
  File &#34;&lt;string&gt;&#34;, line 2, in _prepare_impl
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py&#34;, line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 1288, in _prepare_impl
    self.session.flush()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 4353, in flush
    self._flush(objects)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 4488, in _flush
    with util.safe_reraise():
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py&#34;, line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py&#34;, line 4449, in _flush
    flush_context.execute()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py&#34;, line 466, in execute
    rec.execute(self)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py&#34;, line 642, in execute
    util.preloaded.orm_persistence.save_obj(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py&#34;, line 85, in save_obj
    _emit_update_statements(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py&#34;, line 912, in _emit_update_statements
    c = connection.execute(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1416, in execute
    return meth(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/sql/elements.py&#34;, line 523, in _execute_on_connection
    return connection._execute_clauseelement(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1638, in _execute_clauseelement
    ret = self._execute_context(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1843, in _execute_context
    return self._exec_single_context(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1983, in _exec_single_context
    self._handle_dbapi_exception(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 2352, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py&#34;, line 1964, in _exec_single_context
    self.dialect.do_execute(
  File &#34;/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py&#34;, line 945, in do_execute
    cursor.execute(statement, parameters)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 153, in execute
    result = self._query(query)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py&#34;, line 322, in _query
    conn.query(q)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 822, in _read_query_result
    result.read()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 1200, in read
    first_packet = self.connection._read_packet()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py&#34;, line 772, in _read_packet
    packet.raise_for_error()
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py&#34;, line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File &#34;/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py&#34;, line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1048, &#34;Column &#39;target_user_id&#39; cannot be null&#34;)
[SQL: UPDATE user_action SET target_user_id=%(target_user_id)s WHERE user_action.id = %(user_action_id)s]
[parameters: {&#39;target_user_id&#39;: None, &#39;user_action_id&#39;: 4}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
</textarea>
</div>
<div class="explanation">
  The debugger caught an exception in your WSGI application.  You can now
  look at the traceback which led to the error.  <span class="nojavascript">
  If you enable JavaScript you can also use additional features such as code
  execution (if the evalex feature is enabled), automatic pasting of the
  exceptions and much more.</span>
</div>
      <div class="footer">
        Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
        friendly Werkzeug powered traceback interpreter.
      </div>
    </div>

    <div class="pin-prompt">
      <div class="inner">
        <h3>Console Locked</h3>
        <p>
          The console is locked and needs to be unlocked by entering the PIN.
          You can find the PIN printed out on the standard output of your
          shell that runs the server.
        <form>
          <p>PIN:
            <input type=text name=pin size=14>
            <input type=submit name=btn value="Confirm Pin">
        </form>
      </div>
    </div>
  </body>
</html>

<!--

Traceback (most recent call last):
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1964, in _exec_single_context
    self.dialect.do_execute(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 945, in do_execute
    cursor.execute(statement, parameters)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 153, in execute
    result = self._query(query)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 322, in _query
    conn.query(q)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 822, in _read_query_result
    result.read()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.IntegrityError: (1048, "Column 'target_user_id' cannot be null")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "/home/chris/.local/lib/python3.10/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/home/chris/.local/lib/python3.10/site-packages/flask_jwt_extended/view_decorators.py", line 174, in decorator
    return current_app.ensure_sync(fn)(*args, **kwargs)
  File "/home/chris/novels/backend/app/api/user.py", line 181, in deactivate_account
    result = UserService.deactivate_account(user_id, password)
  File "/home/chris/novels/backend/app/services/user_service.py", line 476, in deactivate_account
    db.session.commit()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/scoping.py", line 599, in commit
    return self._proxied.commit()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 2032, in commit
    trans.commit(_to_root=True)
  File "<string>", line 2, in commit
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1313, in commit
    self._prepare_impl()
  File "<string>", line 2, in _prepare_impl
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 1288, in _prepare_impl
    self.session.flush()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 4353, in flush
    self._flush(objects)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 4488, in _flush
    with util.safe_reraise():
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/session.py", line 4449, in _flush
    flush_context.execute()
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py", line 466, in execute
    rec.execute(self)
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/unitofwork.py", line 642, in execute
    util.preloaded.orm_persistence.save_obj(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py", line 85, in save_obj
    _emit_update_statements(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/orm/persistence.py", line 912, in _emit_update_statements
    c = connection.execute(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1416, in execute
    return meth(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/sql/elements.py", line 523, in _execute_on_connection
    return connection._execute_clauseelement(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1638, in _execute_clauseelement
    ret = self._execute_context(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1843, in _execute_context
    return self._exec_single_context(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1983, in _exec_single_context
    self._handle_dbapi_exception(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2352, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1964, in _exec_single_context
    self.dialect.do_execute(
  File "/home/chris/.local/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 945, in do_execute
    cursor.execute(statement, parameters)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 153, in execute
    result = self._query(query)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/cursors.py", line 322, in _query
    conn.query(q)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 822, in _read_query_result
    result.read()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "/home/chris/.local/lib/python3.10/site-packages/pymysql/err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1048, "Column 'target_user_id' cannot be null")
[SQL: UPDATE user_action SET target_user_id=%(target_user_id)s WHERE user_action.id = %(user_action_id)s]
[parameters: {'target_user_id': None, 'user_action_id': 4}]
(Background on this error at: https://sqlalche.me/e/20/gkpj)


-->

❌ 失败: 请求失败，状态码: 500

## 汇总信息

- 总测试数: 22
- 成功测试数: 20
- 测试通过率: 90.91%
