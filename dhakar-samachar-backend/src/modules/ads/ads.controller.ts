import { Body, Controller, Get, Post } from '@nestjs/common';

@Controller('ads')
export class AdsController {
  @Get()
  list() {
    return { message: 'List advertisements' };
  }

  @Post()
  create(@Body() body: Record<string, unknown>) {
    return { message: 'Create advertisement', body };
  }
}
