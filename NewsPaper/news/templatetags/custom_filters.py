from django import template


register = template.Library()


@register.filter()
def censor(text):
   censored_words = ['Редиска', "редиска"]
   low = text.lower()
   for i in censored_words:
      if i.find(low):
         low = text.replace(i[1:], "*" * (len(i) - 1))

   return f'{low} '