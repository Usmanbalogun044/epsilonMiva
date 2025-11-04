<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\AuthService;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use App\Models\User;
use Illuminate\Support\Facades\Validator;
use Tymon\JWTAuth\Facades\JWTAuth;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    public function __construct(protected AuthService $service)
    {
    }

 
 public function register(Request $request)
{
  $validator = Validator::make($request->all(), [
            'name'     => 'required|string|max:255',
            'email'    => 'required|email|unique:users,email',
            'password' => 'required|string|min:8|confirmed',
        ]);

        // 3. Check if the validation fails
        if ($validator->fails()) {
            return response()->json([
                'message' => 'The given data was invalid.',
                'errors' => $validator->errors()
            ], 422); // 422 is the standard "Unprocessable Entity" code
        }

        // 4. Get the validated data array
        $data = $validator->validated();

        // 5. Create user with a HASHED password
        $user = User::create([
            'name' => $data['name'],
            'email' => $data['email'],
            'password' => Hash::make($data['password']),
        ]);

        // 6. Generate the token
        $token = JWTAuth::fromUser($user);

        // 7. Return the success response
        return response()->json([
            'message' => 'User successfully registered',
            'user' => $user,
            'token' => $token,
            'token_type' => 'bearer',
            'expires_in_minutes' => JWTAuth::factory()->getTTL()
        ], 201); // 201 "Created"
    }


    public function login(Request $request)
    {
        $data = $request->validate([
            'email' => 'required|email',
            'password' => 'required|string',
        ]);

        $result = $this->service->login($data['email'], $data['password']);

        if (! $result) {
            return response()->json(['message' => 'Invalid credentials'], Response::HTTP_UNAUTHORIZED);
        }

        return response()->json($result);
    }

    public function logout(Request $request)
    {
        $user = $request->user();

        if ($user) {
            $this->service->logout($user);
        }

        return response()->json(['message' => 'Logged out']);
    }

    public function me(Request $request)
    {
        return response()->json($request->user());
    }
    
    
}
