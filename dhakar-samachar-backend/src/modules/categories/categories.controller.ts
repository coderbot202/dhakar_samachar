import { Body, Controller, Delete, Get, Param, Post, Put } from '@nestjs/common';

@Controller('categories')
export class CategoriesController {
  @Get()
  list() {
    return { message: 'List categories' };
  }

  @Post()
  create(@Body() body: Record<string, unknown>) {
    return { message: 'Create category', body };
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() body: Record<string, unknown>) {
    return { message: 'Update category', id, body };
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return { message: 'Delete category', id };
  }
}
