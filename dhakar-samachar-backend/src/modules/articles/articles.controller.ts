import { Body, Controller, Delete, Get, Param, Post, Put } from '@nestjs/common';

@Controller('articles')
export class ArticlesController {
  @Get()
  list() {
    return { message: 'List articles' };
  }

  @Get(':slug')
  getBySlug(@Param('slug') slug: string) {
    return { message: 'Get article by slug', slug };
  }

  @Post()
  create(@Body() body: Record<string, unknown>) {
    return { message: 'Create article', body };
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() body: Record<string, unknown>) {
    return { message: 'Update article', id, body };
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return { message: 'Delete article', id };
  }
}
