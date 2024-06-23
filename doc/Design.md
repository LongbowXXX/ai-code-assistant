```plantuml
skinparam package {
    backgroundColor<<plugin>> DarkKhaki
    backgroundColor<<langchain>> Green
}
package "IDE Plugin (kotlin)" <<plugin>> {
    [code_assistant]
}

package "フロントエンド (Python)" <<frontend>> {
    [cli]
    [gui]
}

package "コアロジック (Python)" <<core logic>> {
    [assistant]
}

package "LangChain (Python)" <<langchain>> {
    [langchain]
}

[gui] -down-> [assistant]
[cli] -down-> [assistant]
[code_assistant] ..left-> [cli]
[assistant] -down-> [langchain]
```