import { useInfiniteQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { useInView } from "react-intersection-observer";
import { postService } from "../services/postService";
import { PostMapper } from "./PostMapper";

export const Posts = () => {
  const { data, error, status, fetchNextPage, isFetchingNextPage } =
    useInfiniteQuery({
      queryKey: ["items"],
      queryFn: ({ pageParam }) => postService.getAll(pageParam),
      initialPageParam: 1,
      getNextPageParam: (res) => {
        if (res.data.page < res.data.pages) {
          return res.data.page + 1;
        }
      },
    });

  const { ref, inView } = useInView();

  useEffect(() => {
    if (inView) {
      fetchNextPage();
    }
  }, [fetchNextPage, inView]);

  return (
    <>
      {data?.pages.map((page) => {
        return <PostMapper posts={page.data.items} key={page.data.page} />;
      })}
      <div className="h-2" ref={ref}>
        {isFetchingNextPage && "Loading..."}
      </div>
    </>
  );
};
