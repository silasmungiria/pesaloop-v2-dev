// import { useAssets } from "expo-asset";
// import { ResizeMode, Video } from "expo-av";
// import { Link } from "expo-router";
// import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

// export default function index() {
//   const [assets] = useAssets([require("@/assets/videos/intro.mp4")]);

//   const assetsURL = assets && assets[0] ? assets[0].uri : "";

//   return (
//     <View className="flex-1 justify-between">
//       {/* Video Background */}
//       {assets && (
//         <Video
//           isMuted
//           isLooping
//           shouldPlay
//           resizeMode={ResizeMode.COVER}
//           source={{ uri: assetsURL }}
//           style={styles.video}
//         />
//       )}

//       <View className="flex-1 justify-between bg-black/50">
//         {/* Header */}
//         <View className="px-5 mt-20">
//           <Text className="text-4xl font-extrabold uppercase text-white text-center">
//             Ready to change the way you money?
//           </Text>
//         </View>

//         {/* Buttons */}
//         <View className="flex-row justify-around items-center mb-[15%] px-5">
//           {/* Login Button */}
//           <Link href="/(public)/auth/login" asChild>
//             <TouchableOpacity
//               activeOpacity={0.8}
//               className="bg-gray-900 py-3 px-6 rounded-lg w-[40%] items-center"
//             >
//               <Text className="text-xl text-white">Log in</Text>
//             </TouchableOpacity>
//           </Link>

//           {/* Signup Button */}
//           <Link href="/(public)/auth/signup" asChild>
//             <TouchableOpacity
//               activeOpacity={0.8}
//               className="bg-gray-900 py-3 px-6 rounded-lg w-[40%] items-center"
//             >
//               <Text className="text-xl text-white">Sign up</Text>
//             </TouchableOpacity>
//           </Link>
//         </View>
//       </View>
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   video: {
//     position: "absolute",
//     top: 0,
//     left: 0,
//     width: "100%",
//     height: "100%",
//   },
// });

import { Video, ResizeMode } from "expo-av";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Link } from "expo-router";

const keynoteVideoSource =
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/CastVideos/dash/Google_I_O_2013_KeynoteVideo.mp4";

export default function index() {
  return (
    <View className="flex-1 justify-between bg-gray-100 dark:bg-gray-900">
      {/* Video Background */}
      {keynoteVideoSource && (
        <Video
          isMuted
          isLooping
          shouldPlay
          resizeMode={ResizeMode.COVER}
          source={{ uri: keynoteVideoSource }}
          style={styles.video}
        />
      )}

      <View className="flex-1 justify-between bg-black/50">
        {/* Header */}
        <View className="px-5 mt-20">
          <Text className="text-4xl font-extrabold uppercase text-white text-center">
            Ready to change the way you money?
          </Text>
        </View>

        {/* Buttons */}
        <View className="flex-row justify-around items-center mb-[15%] px-5">
          {/* Login Button */}
          <Link href="/(public)/auth/login" asChild>
            <TouchableOpacity
              activeOpacity={0.8}
              className="bg-gray-900 py-3 px-6 rounded-lg w-[40%] items-center"
            >
              <Text className="text-xl text-white">Log in</Text>
            </TouchableOpacity>
          </Link>

          {/* Signup Button */}
          <Link href="/(public)/auth/signup" asChild>
            <TouchableOpacity
              activeOpacity={0.8}
              className="bg-gray-900 py-3 px-6 rounded-lg w-[40%] items-center"
            >
              <Text className="text-xl text-white">Sign up</Text>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  video: {
    position: "absolute",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
  },
});
