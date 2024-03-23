import emoji


lst_of_emoji = ['😯', '😇', '😅']

for em in lst_of_emoji:
    print(*list(emoji.analyze(em)),'\n')

stroke = 'В этом 👉сообщении😟😟 слишком 🥝🥝 много 😱смайликов😱'

print(emoji.replace_emoji(stroke, ''))