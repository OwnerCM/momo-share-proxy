# encoding:utf-8
import asyncio
from os import environ
from ip import listIP, getheaders, ip_main
from asyncio import create_task, wait, Semaphore, run
from aiohttp import ClientSession, ClientTimeout

global n  # 记录访问成功次数
link = 'link'  # 设置link

# 如果检测到程序在 github actions 内运行，那么读取环境变量中的登录信息
if environ.get('GITHUB_RUN_ID', None):
    link = environ['link']

# 设置代理抓取https页面报错问题解决
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def create_aiohttp(url, proxy_list):
    global n
    n = 0
    async with ClientSession() as session:
        # 生成任务列表
        task = [create_task(web_request(url, proxy, session)) for proxy in proxy_list]
        await wait(task)


# 网页访问
async def web_request(url, proxy, session):
    # 并发限制
    async with Semaphore(10):
        try:
            async with await session.get(url=url, headers=await getheaders(), proxy=proxy,
                                         timeout=ClientTimeout(total=20)) as response:
                # 返回字符串形式的相应数据
                page_source = await response.text()
                await page(page_source)
        except Exception:
            pass


# 判断访问是否成功
async def page(page_source):
    global n
    if "学习天数" in page_source:
        n += 1


def main():
    print(f"访问链接：{link}")
    ip_main()  # 抓取代理
    run(create_aiohttp(link, listIP))
    print(f"墨墨分享链接访问成功{n}次。")


if __name__ == '__main__':
    main()
