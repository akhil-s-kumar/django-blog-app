import graphene
import blogApp.schema

class Query(blogApp.schema.Query, graphene.ObjectType):
    pass

class Mutation(blogApp.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)