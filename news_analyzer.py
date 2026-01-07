#!/usr/bin/env python3
"""
Global Empathy News - News Perspective Gap Analyzer

This script collects news from multiple international sources (CNN, Al Jazeera, Global Times),
groups them by topic, and calculates a "Gap Score" (0-100) indicating the divergence
in perspectives across different news outlets.
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Optional

import feedparser
import google.generativeai as genai


# News source RSS feeds
NEWS_SOURCES = {
    "CNN": {
        "url": "http://rss.cnn.com/rss/edition_world.rss",
        "region": "Western (US)",
        "bias_tendency": "Center-Left"
    },
    "Al Jazeera": {
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "region": "Middle East (Qatar)",
        "bias_tendency": "Center"
    },
    "Global Times": {
        "url": "https://www.globaltimes.cn/rss/outbrain.xml",
        "region": "East Asia (China)",
        "bias_tendency": "State-aligned"
    }
}


def collect_news() -> dict:
    """
    Collect news articles from all configured RSS feeds.
    
    Returns:
        dict: Dictionary with source names as keys and list of articles as values
    """
    all_news = {}
    
    for source_name, source_info in NEWS_SOURCES.items():
        print(f"Fetching news from {source_name}...")
        
        try:
            feed = feedparser.parse(source_info["url"])
            articles = []
            
            for entry in feed.entries[:15]:  # Limit to 15 articles per source
                article = {
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": source_name,
                    "region": source_info["region"],
                    "bias_tendency": source_info["bias_tendency"]
                }
                articles.append(article)
            
            all_news[source_name] = articles
            print(f"  -> Collected {len(articles)} articles from {source_name}")
            
        except Exception as e:
            print(f"  -> Error fetching from {source_name}: {e}")
            all_news[source_name] = []
    
    return all_news


def create_analysis_prompt(news_data: dict) -> str:
    """
    Create a prompt for Gemini API to analyze news and calculate gap scores.
    
    Args:
        news_data: Dictionary containing news articles from all sources
        
    Returns:
        str: Formatted prompt for the API
    """
    # Format news data for the prompt
    news_summary = ""
    for source, articles in news_data.items():
        news_summary += f"\n\n=== {source} ===\n"
        for i, article in enumerate(articles, 1):
            news_summary += f"\n{i}. {article['title']}\n"
            news_summary += f"   Summary: {article['summary'][:300]}...\n" if len(article['summary']) > 300 else f"   Summary: {article['summary']}\n"
    
    prompt = f"""You are a news analysis expert specializing in identifying perspective gaps across international media.

Analyze the following news articles from CNN (Western/US perspective), Al Jazeera (Middle Eastern perspective), and Global Times (Chinese perspective).

{news_summary}

Your task:
1. Identify 3-5 COMMON TOPICS that appear across multiple sources (topics covered by at least 2 sources)
2. For each common topic, analyze the perspective differences between sources
3. Calculate a "Gap Score" (0-100) for each topic:
   - 0-20: Minimal perspective gap (factual reporting, similar framing)
   - 21-40: Low gap (minor differences in emphasis)
   - 41-60: Moderate gap (noticeable differences in framing or focus)
   - 61-80: High gap (significant perspective differences, potential bias)
   - 81-100: Extreme gap (completely opposing narratives or interpretations)

Respond in the following JSON format ONLY (no additional text):
{{
    "analysis_date": "YYYY-MM-DD",
    "topics": [
        {{
            "topic_name": "Topic title",
            "gap_score": 75,
            "gap_level": "High",
            "sources_covering": ["CNN", "Al Jazeera"],
            "perspective_summary": {{
                "CNN": "Brief summary of CNN's perspective",
                "Al Jazeera": "Brief summary of Al Jazeera's perspective",
                "Global Times": "Brief summary or 'Not covered' if not applicable"
            }},
            "key_differences": "Explanation of the main perspective differences",
            "related_articles": [
                {{"source": "CNN", "title": "Article title", "link": "URL"}},
                {{"source": "Al Jazeera", "title": "Article title", "link": "URL"}}
            ]
        }}
    ],
    "overall_gap_score": 65,
    "summary": "Brief overall analysis of the current news landscape perspective gaps"
}}
"""
    return prompt


def analyze_with_gemini(news_data: dict) -> Optional[dict]:
    """
    Use Gemini API to analyze news and calculate gap scores.
    
    Args:
        news_data: Dictionary containing news articles from all sources
        
    Returns:
        dict: Analysis results with gap scores, or None if analysis fails
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = create_analysis_prompt(news_data)
        
        print("\nAnalyzing news with Gemini API...")
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text
        
        # Try to parse JSON from the response
        # Handle potential markdown code blocks
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        
        analysis_result = json.loads(response_text)
        return analysis_result
        
    except json.JSONDecodeError as e:
        print(f"Error parsing Gemini response as JSON: {e}")
        print(f"Raw response: {response_text[:500]}...")
        return None
    except Exception as e:
        print(f"Error during Gemini analysis: {e}")
        return None


def generate_report(analysis: dict, news_data: dict) -> str:
    """
    Generate a human-readable report from the analysis results.
    
    Args:
        analysis: Analysis results from Gemini
        news_data: Original news data
        
    Returns:
        str: Formatted report
    """
    report = []
    report.append("=" * 70)
    report.append("GLOBAL EMPATHY NEWS - Perspective Gap Report")
    report.append("=" * 70)
    report.append(f"\nAnalysis Date: {analysis.get('analysis_date', datetime.now().strftime('%Y-%m-%d'))}")
    report.append(f"Overall Gap Score: {analysis.get('overall_gap_score', 'N/A')}/100")
    report.append(f"\nSummary: {analysis.get('summary', 'No summary available')}")
    
    report.append("\n" + "-" * 70)
    report.append("TOPIC ANALYSIS")
    report.append("-" * 70)
    
    for i, topic in enumerate(analysis.get("topics", []), 1):
        report.append(f"\n{i}. {topic.get('topic_name', 'Unknown Topic')}")
        report.append(f"   Gap Score: {topic.get('gap_score', 'N/A')}/100 ({topic.get('gap_level', 'Unknown')})")
        report.append(f"   Sources: {', '.join(topic.get('sources_covering', []))}")
        report.append(f"\n   Key Differences:")
        report.append(f"   {topic.get('key_differences', 'No differences noted')}")
        
        report.append(f"\n   Perspectives:")
        for source, perspective in topic.get("perspective_summary", {}).items():
            report.append(f"   - {source}: {perspective}")
        
        report.append("")
    
    report.append("\n" + "=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)
    
    return "\n".join(report)


def save_results(analysis: dict, news_data: dict, output_dir: str = "output"):
    """
    Save analysis results to JSON and text files.
    
    Args:
        analysis: Analysis results from Gemini
        news_data: Original news data
        output_dir: Directory to save output files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    # Save raw analysis JSON
    analysis_file = os.path.join(output_dir, f"analysis_{timestamp}.json")
    with open(analysis_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\nAnalysis saved to: {analysis_file}")
    
    # Save raw news data
    news_file = os.path.join(output_dir, f"news_data_{timestamp}.json")
    with open(news_file, "w", encoding="utf-8") as f:
        json.dump(news_data, f, indent=2, ensure_ascii=False)
    print(f"News data saved to: {news_file}")
    
    # Save human-readable report
    report = generate_report(analysis, news_data)
    report_file = os.path.join(output_dir, f"report_{timestamp}.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to: {report_file}")
    
    # Also save latest version for easy access
    latest_analysis = os.path.join(output_dir, "latest_analysis.json")
    with open(latest_analysis, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    latest_report = os.path.join(output_dir, "latest_report.txt")
    with open(latest_report, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nLatest results also saved as:")
    print(f"  - {latest_analysis}")
    print(f"  - {latest_report}")


def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("GLOBAL EMPATHY NEWS - Starting Analysis")
    print("=" * 70)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()
    
    # Step 1: Collect news from all sources
    print("Step 1: Collecting news from sources...")
    news_data = collect_news()
    
    total_articles = sum(len(articles) for articles in news_data.values())
    print(f"\nTotal articles collected: {total_articles}")
    
    if total_articles == 0:
        print("Error: No articles collected. Exiting.")
        return
    
    # Step 2: Analyze with Gemini
    print("\nStep 2: Analyzing perspectives with Gemini AI...")
    analysis = analyze_with_gemini(news_data)
    
    if analysis is None:
        print("Error: Analysis failed. Exiting.")
        return
    
    # Step 3: Save results
    print("\nStep 3: Saving results...")
    save_results(analysis, news_data)
    
    # Step 4: Print summary
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"Overall Gap Score: {analysis.get('overall_gap_score', 'N/A')}/100")
    print(f"Topics Analyzed: {len(analysis.get('topics', []))}")
    
    # Print high-gap topics
    high_gap_topics = [t for t in analysis.get("topics", []) if t.get("gap_score", 0) >= 60]
    if high_gap_topics:
        print(f"\nHigh Gap Topics (score >= 60):")
        for topic in high_gap_topics:
            print(f"  - {topic['topic_name']}: {topic['gap_score']}/100")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
