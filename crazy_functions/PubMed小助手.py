"""
Author: zhangyifan1
Date: 2024-03-21 15:09:37
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-03-21 18:18:31
FilePath: //gpt_academic_zyf//crazy_functions//PubMed小助手.py
Description: 

"""

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


# def Get_Pubmed(keyword, num_of_articels, chatbot, history):
def Get_Pubmed(keyword, chatbot, history):
    from metapub import PubMedFetcher

    print("step3 PubMed小助手 开始运行")
    # initialise the keyword to be searched and number of articles to be retrieved
    keyword = keyword
    print("keyword:", keyword)
    # keyword="sepsis"
    num_of_articles = 10
    print("step4 fetch articles")
    fetch = PubMedFetcher()
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
        print("step7 doi获取完成，下一步是更新ui")
        chatbot[-1] = [chatbot[-1][0], pmid + f"完成搜索！！"]
        yield from update_ui(chatbot=chatbot, history=[])

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
        lambda left, right: pd.merge(left, right, on=["pmid"], how="outer"), data_frames
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

    # 清空历史，以免输入溢出
    history = []
    # meta_paper_info_list = yield from Get_Pubmed(
    #     keyword,
    #     # num_of_articels,
    #     chatbot,
    #     history,
    # )
    print("step2 PubMed小助手 调用Get_Pubmed获取信息")  # 到这里也正常
    meta_paper_info_list = yield from Get_Pubmed(
        keyword,
        # num_of_articels,
        chatbot,
        history,
    )
    # meta_paper_info_list = Get_Pubmed(
    #     keyword,
    #     # num_of_articels,
    #     chatbot,
    #     history,
    # )

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
