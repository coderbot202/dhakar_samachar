import { Body, Controller, Get, Post } from '@nestjs/common';

@Controller('media')
export class MediaController {
  @Post('upload')
  upload(@Body() body: Record<string, unknown>) {
    return { message: 'Upload media', body };
  }

  @Get()
  list() {
    return { message: 'List media files' };
  }
}
