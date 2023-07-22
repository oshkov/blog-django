// Поиск через строку поиска
let textBlock = document.querySelectorAll(".card-text")

let num = 0
let limitSymbols = 300 // Ограничение символов в заметке

while (textBlock.length > num) {
    textArticle = textBlock[num].textContent // В переменную закладывается текст из статьи

    // Если длина текста больше ограничения то будет добавлено многоточие в конце текста
    if (textArticle.length > limitSymbols) { 
        textBlock[num].innerHTML = textArticle.substr(0, limitSymbols) + ' ...'
    }

    num++
}