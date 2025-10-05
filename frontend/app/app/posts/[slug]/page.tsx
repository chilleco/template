import PostDetailView from "@/features/posts/components/post-detail-view";

export default function PostDetailPage({ params }: { params: { slug: string } }) {
  return <PostDetailView slug={params.slug} />;
}
