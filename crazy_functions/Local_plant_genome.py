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


def Search_Info():
    # 输入植物学名
    # 读取本地植物基因组文件
    #
    return


def 植物基因组():

    return
