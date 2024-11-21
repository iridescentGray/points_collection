# points_collection

    此项目用于白嫖微软bing搜索积分

## config

    # 拷贝并完善配置,填充用户名、密码，通知渠道
    cp user_data/config-simple.yaml user_data/config.yaml

### config 解释

    message          执行结果通知渠道
    debug: True      debug模式下,流程会直接执行，不会定时执行
    headless: True   无头执行 (未解之谜: 无头执行时，无法自动登录)、
    execution_interval  执行间隔，避免执行太快，单位是毫秒
    search_times     搜索执行次数

## start-up

### by poetry

    poetry install
    poetry shell
    playwright install --force chromium
    python -m points_collection

### by docker-compose

    # 无头执行，需要提前准备好登陆状态文件 state.json (在有头时跑一遍就行)
    docker-compose up -d

## 待解决问题

    自动登录功能无法在headless时无法运行，有没有大佬来救一下

# 参考

- https://greasyfork.org/zh-CN/scripts/477107-microsoft-bing-rewards%E6%AF%8F%E6%97%A5%E4%BB%BB%E5%8A%A1%E8%84%9A%E6%9C%AC
- https://rewards.bing.com/redeem/ 查看当前积分
