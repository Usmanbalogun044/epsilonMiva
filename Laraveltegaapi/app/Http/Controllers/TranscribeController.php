<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use OpenAI\Laravel\Facades\OpenAI;
use Exception;

class TranscribeController extends Controller
{
    /**
     * Handle the incoming audio transcription request.
     */
    public function transcribe(Request $request)
    {
        // 1. Validation
        $validator = Validator::make($request->all(), [
            'audio' => 'required|file|mimes:mp3,mp4,mpeg,mpga,m4a,wav,webm',
        ]);

        if ($validator->fails()) {
            return response()->json($validator->errors(), 422);
        }

        try {
            // 2. Get the file from the request
            $file = $request->file('audio');
            
            // Get the real path of the uploaded file
            $audioPath = $file->getRealPath();

            // 3. Call the OpenAI Whisper API
            $result = OpenAI::audio()->transcribe([
                'model' => 'whisper-1',
                'file' => fopen($audioPath, 'r'),
                'response_format' => 'json', // You can also get 'text', 'srt', 'vtt'
            ]);

            // 4. Return the successful response
            // The result object has a 'text' property
            return response()->json([
                'transcription' => $result->text,
            ], 200);

        } catch (Exception $e) {
            // Handle API errors or other exceptions
            return response()->json([
                'error' => $e->getMessage(),
            ], 500);
        }
    }
}
