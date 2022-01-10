void main()
{
object oPC = GetLastUsedBy();
object oInvisible_Bookshelf = GetObjectByTag("InvisibleBookcase");
string sShelf_Pair = GetLocalString(OBJECT_SELF,"BookShelf_Pair_Tag");
object oShelf_Pair = GetObjectByTag(sShelf_Pair);
int nSearchDifficulty = GetWillSavingThrow(OBJECT_SELF);
int nListenDifficulty = GetReflexSavingThrow(OBJECT_SELF);
int nLoreDifficulty = GetFortitudeSavingThrow(OBJECT_SELF);
int nSearchSkill = GetSkillRank(SKILL_SEARCH,oPC);
int nListenSkill = GetSkillRank(SKILL_LISTEN,oPC);
int nLoreSkill = GetSkillRank(SKILL_LORE,oPC);
int nOpened = GetLocalInt (OBJECT_SELF,"X2_L_PLC_ACTIVATED_STATE");

    if (nOpened == TRUE)
    {
        ActionPlayAnimation(ANIMATION_PLACEABLE_ACTIVATE);
        SetUseableFlag(OBJECT_SELF,FALSE);
        DelayCommand(10.0,ActionPlayAnimation(ANIMATION_PLACEABLE_DEACTIVATE));
        DelayCommand(25.0,SetUseableFlag(OBJECT_SELF,TRUE));
        SetLocalInt(OBJECT_SELF,"X2_L_PLC_ACTIVATED_STATE",FALSE);
        return;
    }
    if ((nSearchSkill >= nSearchDifficulty))
    {
        ActionPlayAnimation(ANIMATION_PLACEABLE_ACTIVATE);
        AssignCommand(oShelf_Pair,ActionPlayAnimation(ANIMATION_PLACEABLE_ACTIVATE));
        DelayCommand(10.0,AssignCommand(oShelf_Pair,ActionPlayAnimation(ANIMATION_PLACEABLE_DEACTIVATE)));
        SetLocalInt(OBJECT_SELF,"X2_L_PLC_ACTIVATED_STATE",TRUE);
        return;
    }
    if ((nLoreSkill >= nLoreDifficulty))
    {
        FloatingTextStringOnCreature("These books don't seem quite right.",oPC);
        return;
    }

    if ((nListenSkill >= nListenDifficulty))
    {
        FloatingTextStringOnCreature("It sounds hollow behind this.",oPC);
        return;
    }
}
