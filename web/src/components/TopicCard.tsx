import { Topic } from "@/types/analysis";

interface TopicCardProps {
  topic: Topic;
  rank: number;
}

export default function TopicCard({ topic, rank }: TopicCardProps) {
  const getGapLevelStyle = (level: string) => {
    switch (level.toLowerCase()) {
      case "extreme":
        return "border-l-4 border-black";
      case "high":
        return "border-l-4 border-gray-700";
      case "moderate":
        return "border-l-4 border-gray-500";
      default:
        return "border-l-4 border-gray-300";
    }
  };

  return (
    <article
      className={`bg-white p-6 ${getGapLevelStyle(topic.gap_level)} shadow-sm hover:shadow-md transition-shadow`}
    >
      {/* Header */}
      <header className="mb-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-3xl font-light text-gray-400">
              {String(rank).padStart(2, "0")}
            </span>
            <h2 className="text-xl font-semibold leading-tight">
              {topic.topic_name}
            </h2>
          </div>
          <div className="text-right flex-shrink-0">
            <div className="text-3xl font-bold">{topic.gap_score}</div>
            <div className="text-xs uppercase tracking-wider text-gray-500">
              Gap Score
            </div>
          </div>
        </div>
        <div className="mt-2 flex items-center gap-2">
          <span className="text-sm font-medium px-2 py-0.5 bg-gray-100 rounded">
            {topic.gap_level}
          </span>
          <span className="text-sm text-gray-500">
            {topic.sources_covering.join(" · ")}
          </span>
        </div>
      </header>

      {/* Key Differences */}
      <section className="mb-4">
        <p className="text-gray-700 leading-relaxed">{topic.key_differences}</p>
      </section>

      {/* Perspectives */}
      <section className="space-y-3">
        <h3 className="text-xs uppercase tracking-wider text-gray-500 font-medium">
          Perspectives
        </h3>
        <div className="space-y-2">
          {Object.entries(topic.perspective_summary).map(
            ([source, perspective]) =>
              perspective !== "Not covered" && (
                <div key={source} className="pl-3 border-l border-gray-200">
                  <div className="text-sm font-medium text-gray-900">
                    {source}
                  </div>
                  <p className="text-sm text-gray-600 mt-0.5">{perspective}</p>
                </div>
              )
          )}
        </div>
      </section>

      {/* Related Articles */}
      {topic.related_articles.length > 0 && (
        <footer className="mt-4 pt-4 border-t border-gray-100">
          <h3 className="text-xs uppercase tracking-wider text-gray-500 font-medium mb-2">
            Related Articles
          </h3>
          <ul className="space-y-1">
            {topic.related_articles.map((article, index) => (
              <li key={index} className="text-sm">
                <span className="text-gray-500">{article.source}:</span>{" "}
                <a
                  href={article.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-900 hover:underline"
                >
                  {article.title}
                </a>
              </li>
            ))}
          </ul>
        </footer>
      )}
    </article>
  );
}
