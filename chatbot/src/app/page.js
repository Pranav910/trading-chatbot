'use client'

import React, { useState, useEffect, useRef } from "react";
import PromptView from "@/components/PromptView.jsx"
import UserChatComponent from "@/components/UserChatComponent";
import AIChatComponent from "@/components/AIChatComponent";
import { ToastContainer, toast } from "react-toastify";
import './page.css'
import Image from "next/image";
import loading from '../../assets/loading.gif'
import Loader from "@/components/Loader";

export default function Home() {

  const [chats, setChats] = useState([
    {
      'type': 'ai',
      'chat': `## Hello!, Sir
  How can I assist you with market today?`,
      'fileURL': null,
      'sources': null
    }
  // {
  //   type: 'ai',
  //   chat: `AWS (Amazon Web Services) is a comprehensive cloud platform offering a wide range of services. Here are the key points:\n\n1. **Broad Services**: AWS offers over 200 fully featured services, including compute, storage, databases, machine learning, AI, data lakes and analytics, and IoT.\n\n2. **Global Infrastructure**: AWS has an extensive global cloud infrastructure with data centers worldwide, ensuring high availability and reliability.\n\n`,
  //   sources: [
  //       "https://www.amazon.com/favicon.ico",
  //       "https://www.geeksforgeeks.org/favicon.ico",
  //       "https://www.amazon.com/favicon.ico"
  //   ]
  // }
  ])
  const [loadingState, setLoadingState] = useState(false)
  const loadingRef = useRef(null)
  const promptViewRef = useRef(null)
  const [mainPageLoader, setMainPageLoader] = useState(true)

  function setUserChat(userChat, fileURL = null) {
    setChats(p => [...p, {
      type: 'user',
      chat: userChat,
      fileURL
    }])

  }

  function setPromptViewWidth(length) {
    const height = 12 + (length / 73) * 2
    if (promptViewRef.current && height <= 25)
      promptViewRef.current.style.height = `${height}%`
  }

  async function getServerStatus() {

    const res = await fetch("https://bot-service-ufhb.onrender.com", {
      method: 'GET',
    })

    if(res.status === 200){
        setMainPageLoader(false)
      }
  }

  useEffect(() => {

    getServerStatus()

  }, [])

  useEffect(() => {

    if (loadingState == true) {
      loadingRef.current.style.marginBottom = "60px"
      loadingRef.current.scrollIntoView()
    }

  }, [loadingState])

  return (
    <main>

      {
        mainPageLoader? <Loader/>: null
      }

      <h2 className="logo">
        TradingBot
      </h2>

      <ToastContainer toastStyle={{ backgroundColor: '#303030', color: 'white' }} theme="dark" />

      <div className="chats">

        {
          chats.map((chat, index) => {
            if (chat.type == 'user')
              return (
                <div className="humanchat" key={index}>
                  <UserChatComponent chat={chat.chat} fileURL={chat.fileURL} />
                </div>
              )
            else if (chat.type == 'ai')
              return (
                <div key={index} className="aichat">
                  <AIChatComponent chat={chat} loadingState={loadingState} />
                </div>
              )
          })
        }

        {
          loadingState ?
            <div className="aichat loading" ref={loadingRef}>
              <Image width={50} height={50} alt="loading" src={loading} />
            </div> :
            null
        }

      </div>

      <div className="promptview" ref={promptViewRef}>
        <PromptView setUserChat={setUserChat} setChats={setChats} setLoadingState={setLoadingState} setPromptViewWidth={setPromptViewWidth} showToast={toast} />
      </div>
    </main>
  );
}
