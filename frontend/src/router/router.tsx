import { createBrowserRouter } from "react-router-dom";
import { MainLayout } from "../pages/MainLayout";
import { PostPage } from "../pages/PostsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <PostPage />,
      },
    ],
  },
]);
