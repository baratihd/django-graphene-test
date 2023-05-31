import graphene
from graphene_django import DjangoObjectType

from apps.ingredients.models import Category, Ingrediant


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'integrates')


class IngrediantType(DjangoObjectType):

    class Meta:
        model = Ingrediant
        fields = ('id', 'name', 'notes', 'category')


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngrediantType)
    Category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        return Ingrediant.objects.select_related('category').all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return Category.objects.none()


schema = graphene.Schema(query=Query)
