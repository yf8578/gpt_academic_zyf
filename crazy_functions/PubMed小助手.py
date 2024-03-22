"""
Author: zhangyifan1
Date: 2024-03-21 15:09:37
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-03-22 10:55:50
FilePath: //gpt_academic_zyf//crazy_functions//PubMed小助手.py
Description: 

"""

from metapub.exceptions import MetaPubError
from requests.exceptions import ReadTimeout
from concurrent.futures import ThreadPoolExecutor, as_completed
from metapub import PubMedFetcher

# pip install metapub
import pandas as pd
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from toolbox import CatchException, report_exception, promote_file_to_downloadzone
from toolbox import (
    update_ui,
    update_ui_lastest_msg,
    disable_auto_promotion,
    write_history_to_file,
)

print("pubmed小助手起始")


# #####
# #####多线程
# def fetch_article(pmid, fetcher):
#     try:
#         print(f"Fetching article for PMID {pmid}")
#         article = fetcher.article_by_pmid(pmid)
#         print(f"Got article for PMID {pmid}")
#         return {
#             "pmid": pmid,
#             "title": article.title,
#             "abstract": article.abstract,
#             "authors": article.authors,
#             "journal": article.journal,
#             "citation": article.citation,
#             "year": article.year,
#             "issue": article.issue,
#             "link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
#             "doi": article.doi,
#         }
#     except ReadTimeout:
#         print(f"Request timed out: Could not retrieve article info for PMID {pmid}.")
#     except MetaPubError as e:
#         print(
#             f"MetaPub error: {e}. This could be due to non-existent PMID {pmid} or other issues."
#         )


# def Get_Pubmed(keyword, chatbot, history):
#     print("Starting PubMed helper")
#     num_of_articles = 1
#     print("Fetching articles")
#     fetch = PubMedFetcher()
#     print("Fetching...")
#     print("Keyword:", keyword)
#     pmids = fetch.pmids_for_query(keyword, retmax=num_of_articles)
#     print("Fetch complete")
#     print(pmids)
#     print("Iterating over PMIDs")

#     articles_info = []
#     # Use ThreadPoolExecutor to fetch articles in parallel
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         # Create a future for each article fetch
#         future_to_pmid = {
#             executor.submit(fetch_article, pmid, fetch): pmid for pmid in pmids
#         }
#         # As each future completes, process its result
#         for future in as_completed(future_to_pmid):
#             pmid = future_to_pmid[future]
#             try:
#                 article_info = future.result()
#                 if article_info:
#                     articles_info.append(article_info)
#                     print(f"Completed search for PMID {pmid}")
#                     # Update chatbot UI here if necessary
#             except Exception as exc:
#                 print(f"PMID {pmid} generated an exception: {exc}")

#     # Return or process articles_info as needed
#     yield articles_info


# # def Get_Pubmed(keyword, num_of_articels, chatbot, history):
def Get_Pubmed(keyword, chatbot, history):
    from metapub import PubMedFetcher

    print("step3 PubMed小助手 开始运行")
    # initialise the keyword to be searched and number of articles to be retrieved
    keyword = keyword
    # keyword="sepsis"
    num_of_articles = 5
    print("step4 fetch articles")
    fetch = PubMedFetcher()
    print("fetching...")
    print("keyword:", keyword)
    # get the  PMID for first 3 articles with keyword sepsis
    pmids = fetch.pmids_for_query(keyword, retmax=num_of_articles)
    print("step5 fetch done")
    print(pmids)
    # get  articles
    articles = {}
    titles = {}
    abstracts = {}
    authors = {}
    journals = {}
    citation = {}
    years = {}
    issues = {}
    Pmid_dict = {}
    links = {}
    doi = {}
    print("step6 遍历pmids")

    #     for pmid in pmids:
    #         try:
    #             print("step6.1 开始遍历")
    #             article = fetch.article_by_pmid(pmid)
    #             print("step6.2 获取文章")
    #             article_info = {
    #                 "pmid": pmid,
    #                 "title": article.title,
    #                 "abstract": article.abstract,
    #                 "authors": article.authors,
    #                 "journal": article.journal,
    #                 "citation": article.citation,
    #                 "year": article.year,
    #                 "issue": article.issue,
    #                 "link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    #                 "doi": article.doi,
    #             }
    #             print(pmid)
    #             chatbot[-1] = [chatbot[-1][0], pmid + f"完成搜索！！"]
    #             # 注意：这里应该直接调用 update_ui 而不是使用 yield from，因为这不是在生成器中
    #             update_ui(chatbot=chatbot, history=[])
    #         except ReadTimeout:
    #             print(f"请求超时：无法获取PMID {pmid} 的文章信息。")
    #         except MetaPubError as e:
    #             print(f"遇到MetaPub错误：{e}。可能是PMID {pmid} 不存在或其他问题。")

    #         return article_info

    ######
    # 修改前
    #######
    for pmid in pmids:
        print(pmid)
        Pmid_dict[pmid] = pmid
        print(fetch.article_by_pmid(pmid))
        articles[pmid] = fetch.article_by_pmid(pmid)
        titles[pmid] = articles[pmid].title
        abstracts[pmid] = articles[pmid].abstract
        authors[pmid] = articles[pmid].authors
        journals[pmid] = articles[pmid].journal
        citation[pmid] = articles[pmid].citation
        years[pmid] = articles[pmid].year
        issues[pmid] = articles[pmid].issue
        links[pmid] = "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/"
        doi[pmid] = articles[pmid].doi
        # print("step7 doi获取完成，下一步是更新ui")
        # chatbot[-1] = [chatbot[-1][0], pmid + f"完成搜索！！"]
        # yield update_ui(chatbot=chatbot, history=[])

    # create a dataframe
    # Pmid=pd.DataFrame(list(Pmid_dict.items()),columns = ['pmid','pmid'])
    Title = pd.DataFrame(list(titles.items()), columns=["pmid", "Title"])
    Abstract = pd.DataFrame(list(abstracts.items()), columns=["pmid", "Abstract"])
    Author = pd.DataFrame(list(authors.items()), columns=["pmid", "Author"])
    Journal = pd.DataFrame(list(journals.items()), columns=["pmid", "Journal"])
    Citation = pd.DataFrame(list(citation.items()), columns=["pmid", "Citation"])
    Year = pd.DataFrame(list(years.items()), columns=["pmid", "Year"])
    Volume = pd.DataFrame(list(years.items()), columns=["pmid", "Volume"])
    Issue = pd.DataFrame(list(issues.items()), columns=["pmid", "Issue"])
    Link = pd.DataFrame(list(links.items()), columns=["pmid", "Link"])
    Doi = pd.DataFrame(list(doi.items()), columns=["pmid", "Doi"])
    data_frames = [
        Title,
        Abstract,
        Author,
        Year,
        Volume,
        Issue,
        Journal,
        Citation,
        Link,
        Doi,
    ]
    from functools import reduce

    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on=["pmid"], how="outer"),
        data_frames,
    )
    profile = df_merged.to_dict("records")
    # yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面
    print("step4 PubMed小助手 获取信息完成")
    return profile


def PubMed小助手(
    keyword,
    # num_of_articels,
    llm_kwargs,
    plugin_kwargs,
    chatbot,
    history,
    system_prompt,
    user_request,
):
    """
    txt             输入栏用户输入的文本，例如需要翻译的一段话，再例如一个包含了待处理文件的路径
    llm_kwargs      gpt模型参数, 如温度和top_p等, 一般原样传递下去就行
    plugin_kwargs   插件模型的参数，暂时没有用武之地
    chatbot         聊天显示框的句柄，用于显示给用户
    history         聊天历史，前情提要
    system_prompt   给gpt的静默提醒
    user_request    当前用户的请求信息（IP地址等）
    """
    disable_auto_promotion(chatbot=chatbot)
    # 基本信息：功能、贡献者
    chatbot.append(
        [
            "函数插件功能？",
            "分析用户提供的PubMed关键词相关文章：ZYF，插件初始化中...",
        ]
    )
    yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        print("step1 PubMed小助手导入包")  # 正常
        import math

        # from bs4 import BeautifulSoup
    except:
        report_exception(
            chatbot,
            history,
            a=f"解析项目: {keyword}",
            b=f"导入软件依赖失败。使用该模块需要额外依赖，安装方法```pip install --upgrade math arxiv```。",
        )
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
        return

    # data = Get_Pubmed(keyword, chatbot, history)
    # print(data)
    # ######################################
    # ######################################

    # 清空历史，以免输入溢出
    history = []
    # meta_paper_info_list = yield from Get_Pubmed(
    #     keyword,
    #     # num_of_articels,
    #     chatbot,
    #     history,
    # )
    print("step2 PubMed小助手 调用Get_Pubmed获取信息")  # 到这里也正常
    meta_paper_info_list = []

    # # 调用 Get_Pubmed 生成器，并处理每篇文章的信息
    # for article_info in Get_Pubmed(keyword, chatbot, history):
    #     # 这里可以对每篇文章的信息进行处理，例如添加到列表中
    #     meta_paper_info_list.append(article_info)
    # meta_paper_info_list = yield from Get_Pubmed(
    #     keyword,
    #     # num_of_articels,
    #     chatbot,
    #     history,
    # )
    meta_paper_info_list = Get_Pubmed(
        keyword,
        # num_of_articels,
        chatbot,
        history,
    )

    # if len(meta_paper_info_list) == 0:
    #     yield from update_ui_lastest_msg(
    #         lastmsg="获取文献失败，可能触发了反爬机制。",
    #         chatbot=chatbot,
    #         history=history,
    #         delay=0,
    #     )
    #     return
    batchsize = 5
    for batch in range(math.ceil(len(meta_paper_info_list) / batchsize)):
        if len(meta_paper_info_list[:batchsize]) > 0:
            i_say = (
                "下面是一些学术文献的数据，提取出以下内容："
                + "1、英文题目；2、根据相关的生物医学知识，将题目翻译成英文；3、作者；4、发表在哪个Volume；4、引用数量（cite）；5、根据相关的生物医学知识，将abstract翻译成中文；6、发表年份；7、Pubmed对应链接"
                + f"以下是信息源：{str(meta_paper_info_list[:batchsize])}"
            )

            inputs_show_user = (
                f"请分析此关键词：{keyword}相关的文章信息，这是第{batch+1}批"
            )
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say,
                inputs_show_user=inputs_show_user,
                llm_kwargs=llm_kwargs,
                chatbot=chatbot,
                history=[],
                sys_prompt="你是一个学术翻译，请从数据中提取信息。你必须使用Markdown表格。你必须逐个文献进行处理。",
            )

            history.extend([f"第{batch+1}批", gpt_say])
            meta_paper_info_list = meta_paper_info_list[batchsize:]

    chatbot.append(
        [
            "状态？",
            '已经全部完成，您可以试试让AI写一个Related Works，例如您可以继续输入Write a "Related Works" section about "你搜索的研究领域" for me.',
        ]
    )
    msg = "正常"
    yield from update_ui(chatbot=chatbot, history=history, msg=msg)  # 刷新界面
    path = write_history_to_file(history)
    promote_file_to_downloadzone(path, chatbot=chatbot)
    chatbot.append(("完成了吗？", path))
    yield from update_ui(chatbot=chatbot, history=history, msg=msg)  # 刷新界面
