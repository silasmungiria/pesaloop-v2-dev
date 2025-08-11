import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { secureStorage } from "@/features/store";

export interface ContactProp {
  id: string;
  name: string;
  phoneNumbers: string[];
}

interface FrequentContactsStore {
  frequentContacts: ContactProp[];
  setFrequentContacts: (contacts: ContactProp[]) => void;
  addToFrequentContacts: (contact: ContactProp) => void;
  clearFrequentContacts: () => Promise<void>;
}

export const useFrequentContactsStore = create<FrequentContactsStore>()(
  persist(
    (set) => ({
      frequentContacts: [],

      setFrequentContacts: (contacts: ContactProp[]) => {
        set({ frequentContacts: contacts });
      },

      addToFrequentContacts: (contact: ContactProp) => {
        set((state) => {
          const updatedContacts = [...state.frequentContacts];
          const index = updatedContacts.findIndex(
            (item) => item.id === contact.id
          );

          if (index !== -1) {
            updatedContacts.splice(index, 1); // Remove existing
          }
          updatedContacts.unshift(contact); // Add to the top
          return { frequentContacts: updatedContacts.slice(0, 15) }; // Keep only the top 15
        });
      },

      clearFrequentContacts: async () => {
        try {
          set({ frequentContacts: [] });
          await secureStorage.removeItem("frequent-contacts-storage");
        } catch (error) {
          console.error("Failed to reset frequent contacts:", error);
        }
      },
    }),
    {
      name: "frequent-contacts-storage",
      storage: createJSONStorage(() => secureStorage),
      partialize: (state) => ({
        frequentContacts: state.frequentContacts,
      }),
    }
  )
);
