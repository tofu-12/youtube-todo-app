import { getTodayVideos } from "@/lib/api";
import TodoItem from "@/components/TodoItem";

export default async function HomePage() {
  const videos = await getTodayVideos();

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-900">今日のTODO</h1>
      {videos.length === 0 ? (
        <p className="text-gray-500">今日のTODOはありません</p>
      ) : (
        <div className="space-y-3">
          {videos.map((video) => (
            <TodoItem key={video.id} video={video} />
          ))}
        </div>
      )}
    </div>
  );
}
