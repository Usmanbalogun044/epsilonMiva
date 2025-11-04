<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        $connection = Schema::getConnection();
        $driver = $connection->getDriverName();

        if ($driver === 'mysql') {
            // MySQL: change column to JSON
            DB::statement('ALTER TABLE `users` MODIFY `survey` JSON NULL;');
        } elseif ($driver === 'pgsql') {
            // Postgres: convert text to jsonb
            DB::statement("ALTER TABLE users ALTER COLUMN survey TYPE jsonb USING survey::jsonb;");
        } elseif ($driver === 'sqlite') {
            // SQLite has limited ALTER support; drop and recreate column.
            Schema::table('users', function (Blueprint $table) {
                $table->dropColumn('survey');
            });

            Schema::table('users', function (Blueprint $table) {
                $table->json('survey')->nullable()->after('email');
            });
        } else {
            // Fallback: try to change using the schema builder (may require doctrine/dbal)
            Schema::table('users', function (Blueprint $table) {
                $table->json('survey')->nullable()->change();
            });
        }
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        $connection = Schema::getConnection();
        $driver = $connection->getDriverName();

        if ($driver === 'mysql') {
            DB::statement('ALTER TABLE `users` MODIFY `survey` TEXT NULL;');
        } elseif ($driver === 'pgsql') {
            DB::statement("ALTER TABLE users ALTER COLUMN survey TYPE text USING survey::text;");
        } elseif ($driver === 'sqlite') {
            Schema::table('users', function (Blueprint $table) {
                $table->dropColumn('survey');
            });
            Schema::table('users', function (Blueprint $table) {
                $table->string('survey')->nullable()->after('email');
            });
        } else {
            Schema::table('users', function (Blueprint $table) {
                $table->text('survey')->nullable()->change();
            });
        }
    }
};
