## STT_AI_IMAGE_CRAETE

#### 이 프로젝트는 단순히 Azure 를 활용할 목적으로 개발한 프로젝트입니다.
#### Azure 에서 제공하는 기능과을 이용하여 텍스트를 만들고 KALO 를 통해서 이미지를 생성합니다.


_________

###  기능 설명

Azure 에서 사용한 기능은 다음과 같습니다 TTS, STT , Translator 먼저 사용자가 음성으로 생성하고싶은 이미지를 입력합니다.


그입력이 KoNLPy 를 통해 단어 단위로 분리되며 그 단어를 Azure(Translator) 를통해 번역됩니다.


그 번역단어를 NLTK WordNet 에 의해 반의어를 도출해내고 네거티브 프롬프트로 사용되게됩니다.


또한 단어로 쪼개졋던 입력은 다시 문장으로 합쳐 프롬프트로 사용됩니다.


프롬프트와 네거티브 프롬프트를 합쳐 Karlo 로 전송하게되며 Karlo에서 이미지를 생성하게됩니다.

_______

### 기술 스택
+Python

+NLTK

+Kkma (KoNLPy)

+Azure(TTS,STT,Translator)

+Kakao API(Karlo)

+PIL
