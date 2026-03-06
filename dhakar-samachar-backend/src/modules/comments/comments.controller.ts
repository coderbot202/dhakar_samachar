import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';

@Controller('comments')
export class CommentsController {
  @Post()
  create(@Body() body: Record<string, unknown>) {
    return { message: 'Create comment', body };
  }

  @Get('article/:id')
  forArticle(@Param('id') id: string) {
    return { message: 'Get comments for article', id };
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return { message: 'Delete comment', id };
  }
}
