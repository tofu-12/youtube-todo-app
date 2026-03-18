import VideoForm from "@/components/VideoForm";

export default function NewVideoPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-900">動画登録</h1>
      <VideoForm mode="create" />
    </div>
  );
}
