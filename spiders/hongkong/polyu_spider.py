# -*- coding: utf-8 -*-
"""
香港理工大学 (PolyU) 爬虫
目标网址: https://www.polyu.edu.hk/study/pg/taught-postgraduate/find-your-programmes-tpg
"""

import time
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from spiders.base_spider import BaseSpider

class PolyUSpider(BaseSpider):
    def __init__(self, headless: bool = True):
        super().__init__("polyu", headless=headless)
        # self.list_url is automatically derived from config
        self.apply_url = "https://www38.polyu.edu.hk/eAdmission/index.do"

    def run(self) -> List[Dict]:
        print(f"🚀 开始抓取 {self.university_info.get('name', 'PolyU')}...")
        print(f"📍 列表页: {self.list_url}")
        
        self.driver.get(self.list_url)
        
        # 等待列表加载
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "programmes-items"))
            )
            # 稍作等待确保内容渲染
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ 等待项目列表加载超时: {e}")
            return []
            
        # 获取页面源码进行离线解析
        print("📸 抓取页面快照...")
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        results = []
        
        # 查找所有学院区块 (programmes-row)
        # 每个学院都有自己的 programmes-row > programmes-items > views-row 结构
        faculty_blocks = soup.select(".programmes-row")
        print(f"📦 发现 {len(faculty_blocks)} 个学院区块")
        
        for faculty_idx, faculty_block in enumerate(faculty_blocks):
            # 获取学院名称（可选，用于调试）
            faculty_title_el = faculty_block.select_one(".faculty-title")
            faculty_name = faculty_title_el.get_text(strip=True) if faculty_title_el else f"Faculty {faculty_idx+1}"
            
            # 在该学院下查找 programmes-items 容器
            items_container = faculty_block.select_one(".programmes-items")
            if not items_container:
                continue
                
            # 在该容器下查找所有项目行
            items = items_container.select(".views-row")
            print(f"  📚 {faculty_name}: {len(items)} 个项目")
            
            for item in items:
                try:
                    # 提取链接元素
                    link_el = item.select_one("a.programme")
                    if not link_el:
                        continue
                        
                    href = link_el.get("href")
                    if not href:
                        continue
                        
                    # 处理相对链接
                    full_link = href
                    if href.startswith("/"):
                        full_link = "https://www.polyu.edu.hk" + href
                    elif not href.startswith("http"):
                        # 还有可能是相对路径但没有斜杠，视情况而定，PolyU通常是以/开头
                        full_link = "https://www.polyu.edu.hk/" + href
                    
                    # 提取标题
                    title_el = item.select_one(".title")
                    title = title_el.get_text(strip=True) if title_el else ""
                    
                    # 提取副标题 (中文名)
                    subtitle_el = item.select_one(".subtitle")
                    subtitle = subtitle_el.get_text(strip=True) if subtitle_el else ""
                    
                    # 组合名称，方便识别
                    full_name = f"{title} {subtitle}".strip()
                    
                    # 提取截止日期
                    deadline = "N/A"
                    deadline_el = item.select_one(".deadline-section")
                    if deadline_el:
                        # 优先查找 Non-Local
                        non_local_div = deadline_el.find("div", string=lambda t: t and "Non-Local" in t)
                        if non_local_div:
                            raw_dl = non_local_div.get_text(strip=True)
                            # 格式: "Non-Local Application Deadline: 15 Jan 2026 (Main Round)"
                            # 提取冒号后的部分
                            if ":" in raw_dl:
                                deadline = raw_dl.split(":", 1)[1].strip()
                            else:
                                deadline = raw_dl
                        else:
                            # 如果没有 Non-Local，尝试 Local
                            local_div = deadline_el.find("div", string=lambda t: t and "Local" in t)
                            if local_div:
                                 raw_dl = local_div.get_text(strip=True)
                                 if ":" in raw_dl:
                                    deadline = raw_dl.split(":", 1)[1].strip()
                                 else:
                                    deadline = raw_dl
                    
                    # 组合中英文项目名称 (官网原始格式)
                    full_program_name = f"{title} {subtitle}".strip() if subtitle else title
                    
                    # 使用 BaseSpider 的标准模板
                    program_data = self.create_result_template(full_program_name, full_link)
                    program_data["项目deadline"] = deadline
                    program_data["项目申请链接"] = self.apply_url
                    
                    results.append(program_data)
                    
                except Exception as e:
                    print(f"⚠️ 解析条目出错: {e}")
                    continue
                
        # 领导要求：博士项目也要抓取，不再过滤
        print(f"✅ 抓取完成，共 {len(results)} 个项目（包含博士项目）")
        return results

    def filter_doctor_programmes(self, items: List[Dict]) -> List[Dict]:
        """
        过滤博士 (Doctor/PhD) 项目
        """
        filtered = []
        doctor_keywords = ["Doctor", "PhD", "D.B.A.", "EngD", "Philosophy"]
        
        for item in items:
            # 使用正确的字段名 (中文)
            name = item.get("项目名称", "")
            cn_name = item.get("学生案例", "")  # 中文名存储在这里
            
            is_doctor = False
            for kw in doctor_keywords:
                if kw in name:
                    is_doctor = True
                    break
            
            # 也可以检查中文 "博士"
            if "博士" in cn_name:
                is_doctor = True
                
            if not is_doctor:
                filtered.append(item)
            # else:
            #     print(f"🚫 过滤博士项目: {name}")  # 调试用
                
        return filtered

if __name__ == "__main__":
    # 简单的测试运行逻辑
    spider = PolyUSpider(headless=False)
    results = spider.run()
    import json
    print(json.dumps(results, indent=2, ensure_ascii=False))
