import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Categories, Post

class CategoriesType(DjangoObjectType):
    class Meta:
        model = Categories

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class Query(ObjectType):
    category = graphene.Field(CategoriesType, id=graphene.Int())
    post = graphene.Field(PostType, id=graphene.Int())
    categories = graphene.List(CategoriesType)
    posts = graphene.List(PostType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Categories.objects.get(pk=id)

        return None

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Post.objects.get(pk=id)

        return None

    def resolve_categories(self, info, **kwargs):
        return Categories.objects.all()

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

class CategoriesInput(graphene.InputObjectType):
    id = graphene.ID()
    categoryname = graphene.String()

class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    title_tag = graphene.String()
    slug = graphene.String()
    author = graphene.String()
    body = graphene.String()
    category = graphene.String()

class CreateCategories(graphene.Mutation):
    class Arguments:
        input = CategoriesInput(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoriesType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category_instance = Categories(name=input.name)
        category_instance.save()
        return CreateCategories(ok=ok, category=category_instance)

class UpdateCategories(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CategoriesInput(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoriesType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        category_instance = Categories.objects.get(pk=id)
        if category_instance:
            ok = True
            category_instance.name = input.categoryname
            category_instance.save()
            return UpdateCategories(ok=ok, actor=category_instance)
        return UpdateCategories(ok=ok, category=None)

class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        posts = []
        for post_input in input.posts:
          post = Post.objects.get(pk=post_input.id)
          if post is None:
            return CreatePost(ok=False, post=None)
          posts.append(post)
        post_instance = Post(
          title=input.title,
          )
        post_instance.save()
        post_instance.posts.set(posts)
        return CreatePost(ok=ok, post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        post_instance = Post.objects.get(pk=id)
        if post_instance:
            ok = True
            posts = []
            for post_input in input.posts:
              post = Post.objects.get(pk=post_input.id)
              if post is None:
                return UpdatePost(ok=False, post=None)
              posts.append(post)
            post_instance.title=input.title
            post_instance.save()
            post_instance.posts.set(posts)
            return UpdatePost(ok=ok, post=post_instance)
        return UpdatePost(ok=ok, post=None)

class Mutation(graphene.ObjectType):
    create_category = CreateCategories.Field()
    update_category = UpdateCategories.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)