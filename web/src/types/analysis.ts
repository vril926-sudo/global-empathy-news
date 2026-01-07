export interface RelatedArticle {
  source: string;
  title: string;
  link: string;
}

export interface Topic {
  topic_name: string;
  gap_score: number;
  gap_level: string;
  sources_covering: string[];
  perspective_summary: {
    CNN: string;
    "Al Jazeera": string;
    "Global Times": string;
  };
  key_differences: string;
  related_articles: RelatedArticle[];
}

export interface AnalysisData {
  analysis_date: string;
  topics: Topic[];
  overall_gap_score: number;
  summary: string;
}
