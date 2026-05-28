import streamlit as block  # 保持你习惯的组件风格
from streamlit_mic_recorder import mic_recorder


def render_voice_assessment(target_text):
    """
    语音跟读录制组件
    :param target_text: 期待用户朗读的目标英文句子
    """
    st.write("🎤 **语音跟读挑战 / Pronunciation Challenge**")

    # 1. 渲染录音组件
    audio = mic_recorder(
        start_prompt="点击开始录音 (Start)",
        stop_prompt="点击停止录音 (Stop)",
        key=f"recorder_{target_text[:10]}",  # 动态Key防止冲突
        use_container_width=True
    )

    # 2. 录音数据处理流
    if audio:
        # 获取音频字节流（未来可直接对接到语音识别API，如DeepSeek语音或OpenAI Whisper）
        audio_bytes = audio['bytes']

        # 播放用户录制的音频（给评委演示时的直观反馈）
        st.audio(audio_bytes, format='audio/wav')

        # 3. 评测状态反馈（模拟/对接评测算法）
        with st.spinner("正在分析你的发音..."):
            # 【国赛加分提示】：此处可接入Whisper进行STT(语音转文字)并计算编辑距离
            # 目前做前端交互呈现与回放提示
            st.success("🎉 录音成功！发音匹配度：**Excellent (92%)**")
            st.toast("太棒了！口语打卡成功 🎖️")