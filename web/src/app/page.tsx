import { AnalysisData } from "@/types/analysis";
import TopicCard from "@/components/TopicCard";
import analysisData from "../../data/latest_analysis.json";

export default function Home() {
  const data = analysisData as AnalysisData;

  // Sort topics by gap_score in descending order and take top 3
  const topTopics = [...data.topics]
    .sort((a, b) => b.gap_score - a.gap_score)
    .slice(0, 3);

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold tracking-tight">
            Global Empathy News
          </h1>
          <p className="mt-2 text-gray-600">
            Analyzing perspective gaps across international news sources
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Overall Score Section */}
        <section className="mb-12 pb-8 border-b border-gray-200">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
            <div>
              <div className="text-sm uppercase tracking-wider text-gray-500 mb-1">
                Overall Gap Score
              </div>
              <div className="text-6xl font-bold">{data.overall_gap_score}</div>
              <div className="text-sm text-gray-500 mt-1">out of 100</div>
            </div>
            <div className="text-sm text-gray-500">
              Last updated: {data.analysis_date}
            </div>
          </div>
          <p className="mt-6 text-gray-700 leading-relaxed max-w-2xl">
            {data.summary}
          </p>
        </section>

        {/* Topics Section */}
        <section>
          <div className="mb-6">
            <h2 className="text-xl font-semibold">Top Perspective Gaps</h2>
            <p className="text-sm text-gray-500 mt-1">
              Topics with the highest divergence in media coverage
            </p>
          </div>

          <div className="space-y-6">
            {topTopics.map((topic, index) => (
              <TopicCard key={topic.topic_name} topic={topic} rank={index + 1} />
            ))}
          </div>
        </section>

        {/* Sources Info */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h3 className="text-sm uppercase tracking-wider text-gray-500 font-medium mb-4">
            News Sources
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
            <div className="p-4 bg-gray-50">
              <div className="font-medium">CNN</div>
              <div className="text-gray-500">Western (US)</div>
            </div>
            <div className="p-4 bg-gray-50">
              <div className="font-medium">Al Jazeera</div>
              <div className="text-gray-500">Middle East (Qatar)</div>
            </div>
            <div className="p-4 bg-gray-50">
              <div className="font-medium">Global Times</div>
              <div className="text-gray-500">East Asia (China)</div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-12">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <p className="text-sm text-gray-500 text-center">
            Global Empathy News — Understanding different perspectives in global
            news coverage
          </p>
        </div>
      </footer>
    </div>
  );
}
