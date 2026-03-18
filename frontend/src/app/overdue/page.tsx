import { getOverdueVideos } from "@/lib/api";
import TodoItem from "@/components/TodoItem";

export default async function OverduePage() {
  const videos = await getOverdueVideos();

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-900">未実施</h1>
      {videos.length === 0 ? (
        <p className="text-gray-500">未実施の動画はありません</p>
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
