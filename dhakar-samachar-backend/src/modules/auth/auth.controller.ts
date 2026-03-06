import { Body, Controller, Get, Post } from '@nestjs/common';

@Controller('auth')
export class AuthController {
  @Post('login')
  login(@Body() body: { email: string; password: string }) {
    return { message: 'Login endpoint', body };
  }

  @Post('register')
  register(@Body() body: { name: string; email: string; password: string }) {
    return { message: 'Register endpoint', body };
  }

  @Post('refresh')
  refresh(@Body() body: { refreshToken: string }) {
    return { message: 'Refresh endpoint', body };
  }

  @Get('profile')
  profile() {
    return { message: 'Profile endpoint' };
  }
}
