import io from "socket.io-client";
import store from "@/store";

function InitialSocket(module) {
  return io.connect(`${store.state.urls.websocket_url}/${module}`);
}

export const chat_socket = InitialSocket("chat");
chat_socket.on("connect", () => {
  chat_socket.emit("join_self", {cur_id: store.state.user.info.id});
})

