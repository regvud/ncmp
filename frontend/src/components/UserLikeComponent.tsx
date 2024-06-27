import { UserLikeType } from "../types/contentTypes";
import { baseURL } from "../constants/urls";

interface UserLikeMapperProps {
  userLikes: UserLikeType[];
}

export const UserLikeMapper = ({ userLikes }: UserLikeMapperProps) => {
  function avatarClick() {}
  return (
    <div className="flex">
      {userLikes.map(
        (userLike) =>
          userLike.avatar && (
            <img
              className="cursor-pointer w-[50px] rounded-full"
              src={`${baseURL}${userLike.avatar}`}
              key={userLike.userId}
            />
          ),
      )}
    </div>
  );
};
