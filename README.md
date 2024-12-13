# points_collection

    此项目用于白嫖微软bing搜索积分,特性如下:
    1.配置账号密码后，会自动登录微软账号
    2.每天12.30 开始定时执行搜索任务
    3.支持docker 无头运行

## 创建 config

    # 拷贝样例配置
    cp user_data/config-simple.yaml user_data/config.yaml
    # 填充用户名、密码，通知渠道

### config 解释

    message             通知渠道
    debug: True         debug=True时,搜索流程会直接执行，debug=False时,搜索流程会在每天12.30定时执行
    headless: True      无头执行 (未解之谜: 无头执行时，无法自动登录)
    execution_interval  执行间隔，避免执行太快，单位是毫秒
    search_times        搜索执行次数
    microsoft           输入账号密码，自动登录

## start-up

### by pip

    pip install -r requirements.txt
    playwright install --force chromium
    python -m points_collection

### by poetry

    poetry install
    poetry shell
    playwright install --force chromium
    python -m points_collection

### by docker-compose

    # 必须无头执行(设置headless: True)，需要提前在headless: False时，跑一遍自动登录流程,准备好登录态
    docker-compose up -d

## 待解决问题

    自动登录功能无法在headless时无法运行，有没有大佬来救一下

# 参考

- https://greasyfork.org/zh-CN/scripts/477107-microsoft-bing-rewards%E6%AF%8F%E6%97%A5%E4%BB%BB%E5%8A%A1%E8%84%9A%E6%9C%AC
- https://rewards.bing.com/redeem/ 查看当前积分
