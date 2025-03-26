package com.example.codereviewbyaibot.dummy

import android.content.Context
import com.example.burgerheart.dummy.UserProfile
import com.example.codereviewbyaibot.R
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch

// A marker that something could be wrong :)
@OptIn(DelicateCoroutinesApi::class)
// ViewModel doesn't extends androidx.ViewModel
class MainViewModel {

    // It could be better with Dependency Injection
    private val retrofitService = UserProfileRepository()

    // Private modifier is missing. Mutable variable is exposed.
    val uiState = MutableStateFlow<UiState>(UiState.Loading)

    // Context from the outside
    fun prepareText(context: Context) {
        // Placing context reference to the Companion Object
        labelProvider = fun (userProfile: UserProfile): String {
            return if (userProfile.followersCount > 1000) {
                // And here we have a memory leak of Activity
                context.getString(R.string.celebrity)
            } else {
                // And here we have a memory leak of Activity
                context.getString(R.string.user)
            }
        }
    }

    fun loadState() {
        // Global scope instead of viewModelScope.
        // Main Thread, Missing Context (IO, Default)
        GlobalScope.launch {
            uiState.emit(UiState.Loading)
            try {
                val userProfile = retrofitService.service.getUserProfile().userProfile
                uiState.emit(UiState.Loaded(userProfile, labelProvider(userProfile)))
                // TooGenericExceptionCaught
            } catch (e: Exception) {
                uiState.emit(UiState.Error)
            }
        }
    }

    sealed class UiState {
        data object Loading : UiState()

        // Error doesn't have any info
        data object Error : UiState()

        // Should be a data class
        class Loaded(val user: UserProfile, label: String) : UiState()
    }

    companion object {
        // Masking a memory leak into a function, no easy job to spot
        lateinit var labelProvider: (UserProfile) -> String
    }
}