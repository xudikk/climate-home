import datetime

from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImg, Comment, Blog, InfoProduct


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    list_display_links = ["id", 'name', "slug"]


class ImgInline(admin.StackedInline):
    model = ProductImg
    extra = 2


class InfoInline(admin.StackedInline):
    model = InfoProduct
    extra = 5


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty forms to display
    fields = ('user', 'comment')  # Fields to display in the table
    readonly_fields = ('created_at',)  # Make created_at read-only
    can_delete = True  # Allow deletion of comments
    show_change_link = True  # Allow editing individual comments


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "get_price", "ctg", "get_date", "order_count", "display_image"]
    list_display_links = ['id', 'name']
    search_fields = ["name", 'description']
    list_filter = ["price", "ctg", "date", "order_count"]
    inlines = [ImgInline, InfoInline, CommentInline]

    def display_image(self, obj):
        """Admin ro'yxatda kichik rasmni ko'rsatadi."""
        if obj.images.first():
            return format_html(
                '<img src="{}" style="max-height: 75px; max-width: 75px;" />',
                obj.images.first().img.url
            )
        return "Rasm yo'q"

    display_image.short_description = "Rasm"

    @admin.display(empty_value="---")
    def get_date(self, obj):
        hozir = datetime.datetime.now()
        minut = int((hozir - obj.date).total_seconds() // 60)
        if minut == 0:
            return "Hozir"
        if 0 < minut < 60:
            return f"{minut} minut oldin"
        return obj.date.strftime("%H:%M | %d/%m/%Y")

    @admin.display(empty_value="---")
    def get_price(self, obj):
        if obj.discount:
            return format_html(
                f"<del style='color: red;'>{obj.price:,} so'm</del><br> <span style='color: green;'>{obj.get_price()} so'm</span>",
            )
        return obj.org_price()


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "date"]
