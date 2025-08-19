# AI Usage in Cybercrimes  

## Overview  
This repository investigates how AI tools are exploited in cybercriminal ecosystems, using data collected from forums such as 4chan, HackForums, Dread, and Telegram.  
The research includes scraped posts, keyword analysis, visualizations, and a full research paper.  

📄 Full report is not provided for security reasons and Microsoft's safety

---

## Repository Structure  

### Root  
- **AI Usage in Cybercrimes Report.docx** → 5-page research paper with findings  
- **README.md** → Project documentation  

### `/4Chan_scrap`  
- **boards/** → Raw 4chan data dump (thread files)  
- **matches/** → Filtered matches for AI/cybercrime keywords  
- **1_search_thread_titles_and_posts_for_keyword_matches.py** → Script to board raw data dump  
- **2_analyzing_keywords.ipynb** → Jupyter notebook for analyzing results  
- **4Chan_keywords_analysis_results.csv** → Aggregated keyword analysis output  
- **ai_tools_keywords.txt, cybercrimes_keywords.txt, keywords.txt** → Keyword lists used in searches  
- **most_mentioned_ai_tools.png** → Visualization of top AI tools mentioned  

### `/visualization`  
- **AI_cybercrime_Observations.csv** → Data for visualizations  
- **ai_cybercrime_heatmaps.py** → Script to generate heatmaps  
- **platform_vs_tool_counts.csv** → Cross-platform tool usage counts  

---

## Key Findings  
- **LLMs & jailbroken models**: Lower skill barrier for phishing, fraud, and scripting.  
- **Deepfake/voice cloning tools**: Facilitate identity theft and scams.  
- **Efficiency & scale**: AI enables rapid content generation and multilingual phishing.  
- **Cross-platform spread**: Consistent mentions across 4chan, HackForums, Dread, and Telegram.  

---

## Methodology  
1. **Data Collection**: Scraped and filtered 1,000+ posts across multiple forums.  
2. **Keyword Matching**: Applied curated AI and cybercrime keyword lists.  
3. **Analysis**: Quantitative counts + qualitative case studies.  
4. **Visualization**: Generated heatmaps, tool vs. crime correlations.  
5. **Reporting**: Synthesized into a 5-page academic-style paper.  

---

## Citation  
Present in the report 
