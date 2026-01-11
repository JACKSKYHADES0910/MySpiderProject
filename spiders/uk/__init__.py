# -*- coding: utf-8 -*-
"""
英国地区大学爬虫模块

包含的大学:
    - 帝国理工学院 (Imperial College)
    - 曼彻斯特大学 (Manchester)
    - 贝尔法斯特女王大学 (Queen's University Belfast)
    - 阿伯丁大学 (University of Aberdeen)
    - 东英吉利大学 (University of East Anglia)
    - 斯特拉斯克莱德大学 (University of Strathclyde)
    - 伦敦布鲁内尔大学 (Brunel University London)
    - 曼彻斯特城市大学 (Manchester Metropolitan University)
    - 伦敦大学皇家霍洛威学院 (Royal Holloway University of London)
    - 阿尔斯特大学 (Ulster University)
    
TODO: 待添加英国大学爬虫实现
可添加的大学示例:
    - 牛津大学 (Oxford)
    - 剑桥大学 (Cambridge)
    - 伦敦大学学院 (UCL)
    - 伦敦政治经济学院 (LSE)
    等...
"""

from .manchester_spider import ManchesterSpider
from .qub_spider import QUBSpider
from .aberdeen_spider import AberdeenSpider
from .uea_spider import UEASpider
from .strathclyde_spider import StrathclydeSpider
from .brunel_spider import BrunelSpider
from .mmu_spider import MMUSpider
from .royalholloway_spider import RoyalHollowaySpider
from .ulster_spider import UlsterSpider

__all__ = ["ManchesterSpider", "QUBSpider", "AberdeenSpider", "UEASpider", "StrathclydeSpider", "BrunelSpider", "MMUSpider", "RoyalHollowaySpider", "UlsterSpider"]



