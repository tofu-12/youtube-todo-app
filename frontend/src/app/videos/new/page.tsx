import VideoForm from "@/components/VideoForm";

export default function NewVideoPage() {
  return (
    <div>
      <h1 className="mb-4 text-xl font-bold text-gray-900 md:mb-6 md:text-2xl">動画登録</h1>
      <VideoForm mode="create" />
    </div>
  );
}
