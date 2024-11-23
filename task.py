"""
from django.contrib.auth.models import User

user1 = User.objects.create_user('Bober41', 'bober41@example.com', '12345678')
user2 = User.objects.create_user('Medved26', 'medved26@gmail.com', '12345678')


from news.models import Author

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)


from news.models import Category

category1 = Category.objects.create(name='Политика')
category2 = Category.objects.create(name='Автоспорт')
category3 = Category.objects.create(name='Аниме')
category4 = Category.objects.create(name='Игры')
category5 = Category.objects.create(name='Образование')


from news.models import Post

post1 = Post.objects.create(author=author1, post_type=Post.ARTICLE, title='Игры в гонки: 10 лучших автосимуляторов для PC и консолей', content='В последние годы киберспорт развивается невиданными темпами, в призовых фондах международных чемпионатов по видеоиграм появляется всё больше нулей. Автоспорт не остался в стороне от бума киберспорта — Формула-1 даже проводит официальный чемпионат и разыгрывает чемпионские титулы среди виртуальных пилотов.')

post2 = Post.objects.create(author=author2, post_type=Post.ARTICLE, title='Целая жизнь интересного человека и её странной любви, в адекватном аниме от мастера психоделики', content='Есть такие аниме, которые включаешь, чтобы они надругались над вашим мозгом и чувствами, и именно подобными полнометражными шедеврами артхауса прославился режиссер Сатоси Кон. Его работы почти всегда «крайне специфичны», и тем сильнее я был удивлен, увидев произведение, о котором сегодня пойдёт речь. Ведь наш режиссер не только сумел сдержать своё «безумное видение» как надо творить сюжеты, но и пустил это во благо, превратив обычную историю женщины в увлекательное приключение длинной в жизнь. И от него невозможно оторваться, но давайте ближе к делу. С восторгом представляю вам полнометражное аниме «Актриса тысячелетия» (Sennen Joyuu). И по традиции предлагаю быстренько пробежаться по завязке сюжета, чтобы вы понимали, что вас ждёт, а потом я уже подробнее расскажу, чем это аниме удивительно и почему на него стоит потратить своё время.')

post3 = Post.objects.create(author=author1, post_type=Post.NEWS, title='Сенатор оценил сроки готовности доклада комиссии по защите госсуверенитета', content='ПНОМПЕНЬ, 23 ноя - РИА Новости. Ежегодный доклад комиссии СФ по защите госсуверенитета и предотвращению вмешательства во внутренние дела России может быть представлен уже в конце декабря, в нем будет содержаться анализ попыток повлиять на свободный выбор граждан РФ из-за рубежа, заявил РИА Новости глава комиссии Андрей Климов. Он отметил, что, предварительно, итоговый доклад комиссии СФ по защите госсуверенитета будет представлен сенаторам в конце декабря.')


from news.models import PostCategory

post1.categories.add(category4, category2)
post2.categories.add(category3)
post3.categories.add(category1)


from news.models import Comment

comment1 = Comment.objects.create(post=post1, user=user1, content='Играл в Dirt rally 2, игрушка афигенная, жалко руля не было')

comment2 = Comment.objects.create(post=post2, user=user2, content='Обожаю этого автора, ожидал очередную психоделику, разочаровал меня он конечно')

comment3 = Comment.objects.create(post=post2, user=user1, content='Не увлекаюсь анимешками, но автор статьи заинтерисовал меня конечно, пойду посмотрю')

comment4 = Comment.objects.create(post=post3, user=user2, content='Ох уж эта политика...')
post3.dislike()
post3.dislike()
post3.dislike()
post3.dislike()
post3.dislike()
post3.dislike()
post3.like()
post3.like()
comment2.like()
comment2.like()
comment2.like()
comment2.like()
comment2.dislike()
post3.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.dislike()
post1.dislike()
post1.dislike()
post1.dislike()
post1.dislike()
comment1.like()
comment1.like()
post2.dislike()
post2.dislike()
post2.like()
post2.like()
post2.like()
post2.like()
post2.like()
comment3.like()
comment4.dislike()
comment4.dislike()
comment4.dislike()
comment4.dislike()
comment4.dislike()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.order_by('-rating').first()
print(best_author.user.username, best_author.rating)

best_post = Post.objects.order_by('-rating').first()
print(best_post.created_time, best_post.author.user.username,best_post.rating,best_post.title, best_post.preview())

comments = Comment.objects.filter(post=best_post)
for comment in comments: print(comment.created_time, comment.user.username, comment.rating, comment.content)
exit()

"""
