# from json import JSONEncoder
# from django.conf import settings
# from django.forms import Textarea
# from django.forms.util import flatatt
# from django.utils.encoding import smart_unicode
# from django.utils.html import escape
# from django.utils.safestring import mark_safe
#
#
# class MyTinyMCE(Textarea):
#     class Media:
#         js = ('/media/js/tinymce/tinymce.min.js',)
#
#     def __init__(self, language=None, attrs=None):
#         self.language = language or settings.LANGUAGE_CODE[:2]
#         self.attrs = {'class': 'advancededitor'}
#         if attrs: self.attrs.update(attrs)
#         super(MyTinyMCE, self).__init__(attrs)
#
#     def render(self, name, value, attrs=None):
#         rendered = super(MyTinyMCE, self).render(name, value, attrs)
#         return rendered + mark_safe(u'''
#         <script type="text/javascript">
#         tinyMCE.init({
#             mode : "textareas",
#             width : "400",
#             height : "600",
#             theme : 'modern',
#             plugins: "image",
#             language : 'en'
#         });
#         </script>''')
