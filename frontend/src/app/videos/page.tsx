import Link from "next/link";
import { getVideos } from "@/lib/api";

export default async function VideosPage() {
  const videos = await getVideos();

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-900">動画一覧</h1>
      {videos.length === 0 ? (
        <p className="text-gray-500">
          動画が登録されていません。
          <Link href="/videos/new" className="text-blue-600 hover:underline">
            動画を登録
          </Link>
          してください。
        </p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {videos.map((video) => (
            <Link
              key={video.id}
              href={`/videos/${video.id}`}
              className="block rounded-lg border bg-white p-4 shadow-sm hover:shadow-md transition-shadow"
            >
              <h2 className="font-semibold text-gray-900">{video.name}</h2>
              {video.tags.length > 0 && (
                <div className="mt-1 flex flex-wrap gap-1">
                  {video.tags.map((tag) => (
                    <span
                      key={tag.id}
                      className="inline-block rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-800"
                    >
                      {tag.name}
                    </span>
                  ))}
                </div>
              )}
              <div className="mt-2 space-y-0.5 text-sm text-gray-500">
                {video.next_scheduled_date && (
                  <p>次回予定: {video.next_scheduled_date}</p>
                )}
                {video.last_performed_date && (
                  <p>最終実施: {video.last_performed_date}</p>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
