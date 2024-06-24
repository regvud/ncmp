import { UserLikeType } from "../types/contentTypes";
import { baseURL } from "../constants/urls";

interface UserLikeMapperProps {
  userLikes: UserLikeType[];
}

export const UserLikeMapper = ({ userLikes }: UserLikeMapperProps) => {
  return (
    <>
      {userLikes.map(
        (userLike) =>
          userLike.avatar && (
            <img
              className="w-[50px] rounded-full"
              src={`${baseURL}${userLike.avatar}`}
              key={userLike.userId}
            />
          ),
      )}
    </>
  );
};
